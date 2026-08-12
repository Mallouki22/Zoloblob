"""
Risk Manager
"""


class RiskManager:

    def __init__(
        self,
        capital,
        risk=0.01
    ):

        self.capital = capital
        self.risk = risk

    def update_capital(
        self,
        capital
    ):

        self.capital = capital

    def risk_amount(self):

        return self.capital * self.risk