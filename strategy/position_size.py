"""
Position Size Calculator
"""

from mt5.client import MT5Client


class PositionSizer:

    def __init__(self, client=None):

        self.client = client

    def calculate(
    self,
    symbol,
    balance,
    risk_percent,
    stop_loss_distance,
    symbol_info=None
    ):

        if symbol_info is None:

            if self.client is None:
                raise ValueError("MT5Client manquant")

            symbol_info = self.client.symbol_info(symbol)

        if symbol_info is None:
            raise ValueError("Symbole introuvable")

        risk_money = balance * risk_percent

        tick_value = symbol_info.trade_tick_value
        tick_size = symbol_info.trade_tick_size

        if tick_value <= 0 or tick_size <= 0:
            raise ValueError("Tick value invalide")

        loss_per_lot = (
            stop_loss_distance /
            tick_size
        ) * tick_value

        if loss_per_lot <= 0:
            return 0

        lot = risk_money / loss_per_lot

        lot = max(
            symbol_info.volume_min,
            min(
                lot,
                symbol_info.volume_max
            )
        )

        step = symbol_info.volume_step

        # Round down: rounding to the nearest step can exceed the cash risk.
        lot = int(lot / step) * step
        lot = round(lot, 8)

        return lot
    
    
