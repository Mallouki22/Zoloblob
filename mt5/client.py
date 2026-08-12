"""
MT5 Client

Centralise toutes les communications avec MetaTrader 5.
"""

import MetaTrader5 as mt5

from mt5.exceptions import MT5ConnectionError, MT5DataError


class MT5Client:

    def __init__(self):
        self.connected = False

    def initialize(self):
        """
        Initialise la connexion avec MT5.
        """

        if self.connected:
            return True

        if not mt5.initialize():

            raise MT5ConnectionError(
                f"Impossible de connecter MT5 : {mt5.last_error()}"
            )

        self.connected = True

        return True

    def shutdown(self):
        """
        Ferme la connexion MT5.
        """

        if self.connected:
            mt5.shutdown()
            self.connected = False

    def account_info(self):
        """
        Informations du compte.
        """

        if not self.connected:
            self.initialize()

        return mt5.account_info()

    def symbol_info(self, symbol):
        """
        Informations sur un symbole.
        """

        if not self.connected:
            self.initialize()

        return mt5.symbol_info(symbol)

    def get_rates(self, symbol, timeframe, count):

        if not self.connected:
            self.initialize()


        all_rates = []

        chunk = 5000


        remaining = count

        position = 0


        while remaining > 0:

            size = min(
                chunk,
                remaining
            )


            rates = mt5.copy_rates_from_pos(
                symbol,
                timeframe,
                position,
                size
            )


            if rates is None or len(rates) == 0:

                break


            all_rates.append(rates)


            position += size

            remaining -= size


        if not all_rates:

            raise MT5DataError(
                f"Impossible de récupérer les données pour {symbol}"
            )


        import numpy as np


        return np.concatenate(
            all_rates
        )

    def find_symbol(
        self,
        keyword
    ):

        if not self.connected:
            self.initialize()

        symbols = mt5.symbols_get()

        if symbols is None:
            raise MT5DataError(
                "Impossible de récupérer les symboles."
            )

        keyword = keyword.upper()

        std_symbol = None
        crp_symbol = None
        normal_symbol = None

        for symbol in symbols:

            name = symbol.name.upper()

            if keyword not in name:
                continue

            if not symbol.visible:
                mt5.symbol_select(symbol.name, True)

            # Priorité 1 : -STD
            if name.endswith("-STD"):

                std_symbol = symbol.name

            # Priorité 2 : .CRP
            elif ".CRP" in name:

                crp_symbol = symbol.name

            # Priorité 3 : XAUUSD
            elif name == keyword:

                normal_symbol = symbol.name

        if std_symbol:

            print("📊 Symbole utilisé :", std_symbol)
            return std_symbol

        if crp_symbol:

            print("📊 Symbole utilisé :", crp_symbol)
            return crp_symbol

        if normal_symbol:

            print("📊 Symbole utilisé :", normal_symbol)
            return normal_symbol

        raise MT5DataError(
            f"Aucun symbole trouvé pour {keyword}"
        )
    
    def symbol_tick(self, symbol):

        if not self.connected:
            self.initialize()

        return mt5.symbol_info_tick(symbol)


    def send_order(self, request):

        if not self.connected:
            self.initialize()

        return mt5.order_send(request)
    
    def positions(self):

        if not self.connected:
            self.initialize()

        positions = mt5.positions_get()

        if positions is None:
            return []

        return positions
    
    def filling_mode(self, symbol):

        info = self.symbol_info(symbol)

        if info is None:
            raise ValueError("Symbole introuvable")

        return info.filling_mode