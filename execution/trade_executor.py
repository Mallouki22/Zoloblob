"""
Trade Executor
"""

import MetaTrader5 as mt5

from strategy.position_size import PositionSizer
from utils.logger import TradingLogger
from risk.live_guard import LiveRiskGuard
from execution.trade_validator import TradeValidator

from config.settings import (
    MAGIC_NUMBER,
    MAX_CONSECUTIVE_LOSSES,
    MAX_DAILY_LOSS,
)
from trade.trade_planner import TradePlanner


class TradeExecutor:

    def __init__(
        self,
        order_manager,
        position_manager,
        risk_manager,
    ):

        self.order_manager = order_manager
        self.position_manager = position_manager
        self.risk_manager = risk_manager

        self.sizer = PositionSizer(
            client=self.order_manager.client
        )

        self.logger = TradingLogger()

        self.risk_guard = LiveRiskGuard(
            max_daily_loss=MAX_DAILY_LOSS,
            max_consecutive_losses=MAX_CONSECUTIVE_LOSSES,
            magic_number=MAGIC_NUMBER,
        )

        self.validator = TradeValidator(
            position_manager=self.position_manager,
            order_manager=self.order_manager,
            risk_guard=self.risk_guard,
        )
        self.planner = TradePlanner()

    def execute(
        self,
        prediction,
        symbol,
    ):

        account = self.order_manager.client.account_info()

        if account is None:
            return False

        allowed, reason = self.validator.check(
            prediction=prediction,
            symbol=symbol,
            account=account,
        )

        print("TradeValidator :", allowed, reason)

        if not allowed:

            print("🚫 Trade refusé :", reason)

            self.logger.log(
                symbol,
                prediction,
                entry,
                sl,
                lot,
                status,
            )
            return False

        signal = prediction["signal"]

        tick = self.order_manager.client.symbol_tick(symbol)

        if tick is None:

            print("❌ Tick indisponible.")

            return False

        if signal == "BUY":

            entry = tick.ask

        else:

            entry = tick.bid

        plan = self.planner.build(
            prediction["market"].iloc[-1:],
            1 if signal == "BUY" else -1,
        )

        if plan is None:

            print("❌ Impossible de construire le plan.")

            return False

        sl = plan["sl"]

        tp1 = plan["tp1"]

        tp2 = plan["tp2"]

        tp3 = plan["tp3"]

        stop_distance = plan["risk"]
        prediction["sl"] = sl
        prediction["tp1"] = tp1
        prediction["tp2"] = tp2
        prediction["tp3"] = tp3
        prediction["risk"] = plan["risk"]

        lot = self.sizer.calculate(
            symbol=symbol,
            balance=account.balance,
            risk_percent=self.risk_manager.risk,
            stop_loss_distance=stop_distance,
        )

        print("\n===== TRADE =====")
        print("Signal :", signal)
        print("Entry  :", entry)
        print("Lot    :", lot)
        print("SL     :", sl)
        print("TP1 :", tp1)
        print("TP2 :", tp2)
        print("TP3 :", tp3)
        print("Risk :", plan["risk"])
        print("Score:", prediction["score"])
        if signal == "BUY":

            results = self.order_manager.buy_multi(

                symbol,

                lot,

                sl,

                tp1,

                tp2,

                tp3,
            )

        else:

            results = self.order_manager.sell_multi(

                symbol,

                lot,

                sl,

                tp1,

                tp2,

                tp3,
            )

        status = "FAILED"

        for result in results:

            if result is not None:

                if result.retcode == mt5.TRADE_RETCODE_DONE:

                    status = "OPENED"

        self.logger.log(
            symbol,
            prediction,
            entry,
            sl,
            lot,
            status,
        )

        return status == "OPENED"