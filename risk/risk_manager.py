class RiskManager:

    def __init__(self, risk=0.01):
        self.risk = risk

    def compute_risk(self, capital):
        return capital * self.risk

    def update_after_trade(
        self,
        capital,
        profit
    ):
        return capital + profit