"""
Position Monitor

Surveille les positions ouvertes et applique
le Break Even et le Trailing Stop.
"""

import MetaTrader5 as mt5

from strategy.breakeven import BreakEvenManager
from strategy.trailing import TrailingStopManager

from config.settings import (
    BREAK_EVEN_ATR_TRIGGER,
    ENABLE_BREAK_EVEN,
    ENABLE_TRAILING_STOP,
    TRAILING_ATR_MULTIPLIER,
)


class PositionMonitor:

    def __init__(self, position_manager):

        self.position_manager = position_manager

        self.break_even = BreakEvenManager()

        self.trailing = TrailingStopManager()

    def update(
        self,
        atr_by_symbol=None,
    ):

        if (
            not ENABLE_BREAK_EVEN
            and not ENABLE_TRAILING_STOP
        ):
            return

        atr_by_symbol = atr_by_symbol or {}

        positions = self.position_manager.get_positions()

        if not positions:
            return

        for position in positions:

            atr = atr_by_symbol.get(position.symbol)

            if atr is None or atr <= 0:
                continue

            self.manage(
                position,
                atr,
            )

    def manage(
        self,
        position,
        atr,
    ):

        tick = self.position_manager.client.symbol_tick(
            position.symbol
        )

        if tick is None:
            return

        signal = (
            "BUY"
            if position.type == mt5.POSITION_TYPE_BUY
            else "SELL"
        )

        current_price = (
            tick.bid
            if signal == "BUY"
            else tick.ask
        )

        print("\n===== POSITION =====")
        print("Ticket  :", position.ticket)
        print("Symbol  :", position.symbol)
        print("Profit  :", position.profit)
        print("Entry   :", position.price_open)
        print("Current :", current_price)
        print("SL      :", position.sl)
        print("TP      :", position.tp)

        # -------------------------
        # BREAK EVEN
        # -------------------------

        if ENABLE_BREAK_EVEN:

            move = self.break_even.should_move(
                signal=signal,
                entry=position.price_open,
                current=current_price,
                atr=atr * BREAK_EVEN_ATR_TRIGGER,
            )

            if move:

                be_price = self.break_even.break_even_price(
                    signal=signal,
                    entry=position.price_open,
                )

                if abs(position.sl - be_price) > 1e-5:

                    print("🟢 BREAK EVEN")

                    self.position_manager.move_to_break_even(
                        position,
                    )

        # -------------------------
        # TRAILING
        # -------------------------

        if not ENABLE_TRAILING_STOP:
            return

        new_sl = self.trailing.calculate(
            signal=signal,
            current_price=current_price,
            atr=atr * TRAILING_ATR_MULTIPLIER,
        )

        if self.trailing.should_update(
            signal=signal,
            current_sl=position.sl,
            new_sl=new_sl,
        ):

            print("📈 TRAILING STOP")

            self.position_manager.move_stop(
                position,
                new_sl,
            )