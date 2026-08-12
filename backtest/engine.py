"""Conservative, bar-based simulation of the live trading rules.

Signals are known at a candle close and are executed at the following candle
open. When a stop and a target are both reachable in a candle, the stop wins.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd

from config.settings import (
    ATR_MULTIPLIER, BACKTEST_COMMISSION_PER_LOT_ROUND_TURN,
    BACKTEST_CONTRACT_SIZE, BACKTEST_FALLBACK_SPREAD_POINTS,
    BACKTEST_FORCE_CLOSE_AT_END, BACKTEST_POINT_SIZE, BACKTEST_SLIPPAGE_POINTS,
    BREAK_EVEN_ATR_TRIGGER, ENABLE_BREAK_EVEN, ENABLE_TRAILING_STOP,
    MAX_CONSECUTIVE_LOSSES, MAX_DAILY_LOSS, MAX_OPEN_TRADES, RISK_PERCENT,
    RISK_REWARD_RATIO, TRAILING_ATR_MULTIPLIER,
)
from risk.guard import RiskGuard
from strategy.filter import TradeFilter
from strategy.stoploss import StopLossManager
from strategy.takeprofit import TakeProfitManager


@dataclass
class SimulatedPosition:
    direction: str
    entry: float
    stop: float
    target: float
    atr: float
    lot: float
    opened_at: object
    commission: float
    pending_stop: float | None = None


class BacktestEngine:
    def __init__(
        self, df: pd.DataFrame, predictions, confidence, capital: float = 10_000.0,
        risk: float = RISK_PERCENT, atr_multiplier: float = ATR_MULTIPLIER,
        reward_ratio: float = RISK_REWARD_RATIO, confidence_threshold: float | None = None,
        max_open_positions: int = MAX_OPEN_TRADES, point_size: float = BACKTEST_POINT_SIZE,
        fallback_spread_points: float = BACKTEST_FALLBACK_SPREAD_POINTS,
        slippage_points: float = BACKTEST_SLIPPAGE_POINTS,
        commission_per_lot_round_turn: float = BACKTEST_COMMISSION_PER_LOT_ROUND_TURN,
        contract_size: float = BACKTEST_CONTRACT_SIZE,
        enable_break_even: bool = ENABLE_BREAK_EVEN,
        enable_trailing_stop: bool = ENABLE_TRAILING_STOP,
        force_close_at_end: bool = BACKTEST_FORCE_CLOSE_AT_END, **legacy_options,
    ):
        if len(df) != len(predictions) or len(df) != len(confidence):
            raise ValueError("df, predictions and confidence must have identical lengths")
        required = {"open", "high", "low", "close", "ATR"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Backtest data is missing required columns: {sorted(missing)}")

        self.df = df.reset_index(drop=True).copy()
        self.predictions = list(predictions)
        self.confidence = list(confidence)
        self.initial_capital = capital
        self.capital = capital
        self.risk = risk
        self.point_size = point_size
        self.fallback_spread_points = fallback_spread_points
        self.slippage_points = slippage_points
        self.commission_per_lot_round_turn = commission_per_lot_round_turn
        self.contract_size = contract_size
        self.force_close_at_end = force_close_at_end
        self.enable_break_even = enable_break_even
        self.enable_trailing_stop = enable_trailing_stop
        self.break_even_trigger = BREAK_EVEN_ATR_TRIGGER
        self.trailing_multiplier = TRAILING_ATR_MULTIPLIER
        self.positions: list[SimulatedPosition] = []
        self.trades: list[dict] = []
        self.balance_history = [capital]
        self.pending_signal: tuple[str, float, object] | None = None
        self.stoploss = StopLossManager(multiplier=atr_multiplier)
        self.takeprofit = TakeProfitManager(ratio=reward_ratio)
        threshold = confidence_threshold if confidence_threshold is not None else 0.70
        self.filter = TradeFilter(
            buy_min_confidence=threshold, sell_min_confidence=threshold,
            max_open_trades=max_open_positions,
        )
        self.risk_guard = RiskGuard(MAX_DAILY_LOSS, MAX_CONSECUTIVE_LOSSES)
        self.rejections: dict[str, int] = {}

    def run(self) -> pd.DataFrame:
        for index, row in self.df.iterrows():
            current_time = row.get("time", index)
            self._open_pending(row, current_time)
            self._process_positions(row, current_time)
            self._queue_signal(index, current_time)
        if self.force_close_at_end and self.positions:
            row = self.df.iloc[-1]
            for position in list(self.positions):
                self._close(position, row["close"], "END_OF_DATA", row.get("time", len(self.df) - 1))
        return pd.DataFrame(self.trades)

    def _queue_signal(self, index: int, signal_time: object) -> None:
        signal = {0: "SELL", 1: "WAIT", 2: "BUY"}.get(self.predictions[index])
        if signal is not None:
            self.pending_signal = (signal, float(self.confidence[index]), signal_time)

    def _open_pending(self, row: pd.Series, current_time: object) -> None:
        if self.pending_signal is None:
            return
        signal, confidence, _ = self.pending_signal
        self.pending_signal = None
        allowed, reason = self.risk_guard.can_open(self.capital, self._date_of(current_time))
        if not allowed:
            self._reject(reason)
            return
        spread_points = float(row.get("spread", self.fallback_spread_points))
        if pd.isna(spread_points):
            spread_points = self.fallback_spread_points
        allowed, reason = self._check_signal({"signal": signal, "confidence": confidence}, spread_points)
        if not allowed:
            self._reject(reason)
            return
        atr = float(row["ATR"])
        if not pd.notna(atr) or atr <= 0:
            self._reject("ATR invalide")
            return
        side = 1 if signal == "BUY" else -1
        entry_cost = (spread_points + self.slippage_points) * self.point_size
        entry = float(row["open"]) + (entry_cost if side == 1 else -self.slippage_points * self.point_size)
        stop, distance = self.stoploss.calculate(signal, entry, atr)
        target = self.takeprofit.calculate(signal, entry, distance)
        lot = (self.capital * self.risk) / (distance * self.contract_size)
        if lot <= 0:
            self._reject("Taille de position nulle")
            return
        self.positions.append(SimulatedPosition(
            direction=signal, entry=entry, stop=stop, target=target, atr=atr,
            lot=lot, opened_at=current_time,
            commission=lot * self.commission_per_lot_round_turn,
        ))

    def _check_signal(self, prediction: dict, spread_points: float) -> tuple[bool, str]:
        signal = prediction["signal"]
        if signal == "WAIT":
            return False, "Signal WAIT"
        if prediction["confidence"] < self.filter.required_confidence(signal):
            return False, "Confiance insuffisante"
        if spread_points > self.filter.max_spread:
            return False, "Spread trop élevé"
        if len(self.positions) >= self.filter.max_open_trades:
            return False, "Nombre maximal de positions atteint"
        return True, "OK"

    def _process_positions(self, row: pd.Series, current_time: object) -> None:
        for position in list(self.positions):
            if position.pending_stop is not None:
                position.stop = position.pending_stop
                position.pending_stop = None
            if self._exit_hit(position, row):
                continue
            self._schedule_protection(position, float(row["close"]))

    def _exit_hit(self, position: SimulatedPosition, row: pd.Series) -> bool:
        if position.direction == "BUY":
            stop_hit, target_hit = row["low"] <= position.stop, row["high"] >= position.target
        else:
            stop_hit, target_hit = row["high"] >= position.stop, row["low"] <= position.target
        if stop_hit:  # Conservative when stop and target are both touched.
            self._close(position, position.stop, "STOP", row.get("time"))
            return True
        if target_hit:
            self._close(position, position.target, "TARGET", row.get("time"))
            return True
        return False

    def _schedule_protection(self, position: SimulatedPosition, close: float) -> None:
        next_stop = position.stop
        if position.direction == "BUY":
            if self.enable_break_even and close >= position.entry + position.atr * self.break_even_trigger:
                next_stop = max(next_stop, position.entry)
            if self.enable_trailing_stop:
                next_stop = max(next_stop, close - position.atr * self.trailing_multiplier)
            if next_stop > position.stop:
                position.pending_stop = next_stop
        else:
            if self.enable_break_even and close <= position.entry - position.atr * self.break_even_trigger:
                next_stop = min(next_stop, position.entry)
            if self.enable_trailing_stop:
                next_stop = min(next_stop, close + position.atr * self.trailing_multiplier)
            if next_stop < position.stop:
                position.pending_stop = next_stop

    def _close(self, position: SimulatedPosition, raw_exit: float, reason: str, closed_at: object) -> None:
        slip = self.slippage_points * self.point_size
        exit_price = raw_exit - slip if position.direction == "BUY" else raw_exit + slip
        sign = 1 if position.direction == "BUY" else -1
        gross = (exit_price - position.entry) * sign * position.lot * self.contract_size
        pnl = gross - position.commission
        self.capital += pnl
        self.balance_history.append(self.capital)
        self.risk_guard.record_closed_trade(pnl)
        self.trades.append({
            "direction": position.direction, "opened_at": position.opened_at,
            "closed_at": closed_at, "entry": position.entry, "exit": exit_price,
            "stop": position.stop, "target": position.target, "lot": position.lot,
            "result": "WIN" if pnl > 0 else "LOSS", "exit_reason": reason,
            "gross_profit": gross, "cost": position.commission, "profit": pnl,
            "balance": self.capital,
        })
        self.positions.remove(position)

    def _date_of(self, value: object) -> date:
        try:
            return pd.Timestamp(value).date()
        except (TypeError, ValueError):
            return date.today()

    def _reject(self, reason: str) -> None:
        self.rejections[reason] = self.rejections.get(reason, 0) + 1
