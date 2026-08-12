"""
Order Manager
"""

import MetaTrader5 as mt5

from mt5.client import MT5Client
from config.settings import (
    MAGIC_NUMBER,
    DEVIATION
)


class OrderManager:

    from config.settings import (
        TP1_VOLUME,
        TP2_VOLUME,
        TP3_VOLUME,
    )
    def __init__(self):

        self.client = MT5Client()
        self.client.initialize()


    def _send(self, symbol, volume, order_type, sl, tp):

        tick = self.client.symbol_tick(symbol)

        if tick is None:
            print("❌ Tick introuvable")
            return None

        price = (
            tick.ask
            if order_type == mt5.ORDER_TYPE_BUY
            else tick.bid
        )

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": DEVIATION,
            "magic": MAGIC_NUMBER,
            "comment": "AI Trading Bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
           }
        print("\n===== ORDER REQUEST =====")

        for key, value in request.items():

            print(f"{key} : {value}")
        result = self.client.send_order(request)

        if result is None:
            print("❌ order_send() a retourné None")
            return None

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("❌ Erreur MT5 :", result.retcode)
            print(result)
            return result

        print("✅ Ordre exécuté")
        print("Ticket :", result.order)

        return result


    def buy(self, symbol, volume, sl, tp):

        return self._send(
            symbol,
            volume,
            mt5.ORDER_TYPE_BUY,
            sl,
            tp
        )


    def sell(self, symbol, volume, sl, tp):

        return self._send(
            symbol,
            volume,
            mt5.ORDER_TYPE_SELL,
            sl,
            tp
        )
    def buy_multi(
        self,
        symbol,
        total_volume,
        sl,
        tp1,
        tp2,
        tp3,
    ):

        volumes = [
            round(total_volume * TP1_VOLUME, 2),
            round(total_volume * TP2_VOLUME, 2),
            round(total_volume * TP3_VOLUME, 2),
        ]

        results = []

        for volume, tp in zip(volumes, [tp1, tp2, tp3]):

            if volume > 0:

                results.append(
                    self.buy(
                        symbol,
                        volume,
                        sl,
                        tp,
                    )
                )

        return results

    def sell_multi(
        self,
        symbol,
        total_volume,
        sl,
        tp1,
        tp2,
        tp3,
    ):

        volumes = [
            round(total_volume * TP1_VOLUME, 2),
            round(total_volume * TP2_VOLUME, 2),
            round(total_volume * TP3_VOLUME, 2),
        ]

        results = []

        for volume, tp in zip(volumes, [tp1, tp2, tp3]):

            if volume > 0:

                results.append(
                    self.sell(
                        symbol,
                        volume,
                        sl,
                        tp,
                    )
                )

        return results