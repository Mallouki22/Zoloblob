"""
Professional Money Manager
"""


class MoneyManager:

    def __init__(self):

        pass

    def compute_lot(
        self,
        capital,
        risk_percent,
        entry,
        stop,
        contract_size=100,
    ):

        risk_money = capital * risk_percent

        stop_distance = abs(
            entry - stop
        )

        if stop_distance <= 0:
            return 0

        lot = (
            risk_money /
            (
                stop_distance *
                contract_size
            )
        )

        return round(
            lot,
            2
        )