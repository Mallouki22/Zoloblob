class MT5ConnectionError(Exception):
    """Erreur lors de la connexion à MetaTrader 5."""
    pass


class MT5SymbolError(Exception):
    """Erreur liée à un symbole MT5."""
    pass


class MT5DataError(Exception):
    """Erreur lors de la récupération des données."""
    pass