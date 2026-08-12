"""
Position Manager

Gestion des positions ouvertes.
"""

import MetaTrader5 as mt5

from mt5.client import MT5Client


class PositionManager:

    def __init__(self):

        self.client = MT5Client()

        self.client.initialize()

    def get_positions(self, symbol=None):

        if symbol is None:
            positions = mt5.positions_get()

        else:
            positions = mt5.positions_get(
                symbol=symbol
            )

        if positions is None:
            return []

        return list(positions)

    def has_position(self, symbol=None):

        return len(
            self.get_positions(symbol)
        ) > 0

    def count(self, symbol=None):

        return len(
            self.get_positions(symbol)
        )

    def total_profit(self):

        positions = self.get_positions()

        return sum(
            position.profit
            for position in positions
        )
    def update_stop_loss(
        self,
        ticket,
        new_sl,
        tp
    ):

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": ticket,

            "sl": new_sl,

            "tp": tp

        }

        return mt5.order_send(request)
    def get_position_by_ticket(
        self,
        ticket
    ):

        positions = self.get_positions()

        for position in positions:

            if position.ticket == ticket:

                return position

        return None

    def close_position(
        self,
        ticket
    ):

        print(
            f"Fermeture position {ticket}"
        )

        # à implémenter plus tard
    
    def positions_by_direction(
        self,
        symbol,
        signal,
    ):

        positions = self.get_positions(symbol)

        if signal == "BUY":

            return [
                p
                for p in positions
                if p.type == mt5.POSITION_TYPE_BUY
            ]

        return [
            p
            for p in positions
            if p.type == mt5.POSITION_TYPE_SELL
        ]

    def count_direction(
        self,
        symbol,
        signal,
    ):

        return len(
            self.positions_by_direction(
                symbol,
                signal,
            )
        )
    def move_to_break_even(
        self,
        position,
    ):

        return self.update_stop_loss(
            ticket=position.ticket,
            new_sl=position.price_open,
            tp=position.tp,
        )
    def move_stop(
        self,
        position,
        new_sl,
    ):

        return self.update_stop_loss(
            ticket=position.ticket,
            new_sl=new_sl,
            tp=position.tp,
        )
    def profit_points(
        self,
        position,
    ):

        tick = self.client.symbol_tick(position.symbol)

        if tick is None:

            return 0

        if position.type == mt5.POSITION_TYPE_BUY:

            return tick.bid - position.price_open

        return position.price_open - tick.ask