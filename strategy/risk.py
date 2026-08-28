"""
Risk Manager
"""

from __future__ import annotations


class RiskManager:

    def __init__(
        self,
        capital,
        risk=0.005,
        max_daily_loss=0.01,
        max_consecutive_losses=3,
    ):

        self.capital = float(capital)
        self.risk = float(risk)

        self.max_daily_loss = float(
            max_daily_loss
        )

        self.max_consecutive_losses = int(
            max_consecutive_losses
        )

        self.daily_loss = 0.0
        self.consecutive_losses = 0

    def update_capital(self, capital):

        self.capital = float(capital)

    def risk_amount(self):

        return self.capital * self.risk

    def daily_loss_limit(self):

        return self.capital * self.max_daily_loss

    def can_trade(self):

        if self.daily_loss >= self.daily_loss_limit():
            return False

        if (
            self.consecutive_losses
            >= self.max_consecutive_losses
        ):
            return False

        return True

    def register_win(self):

        self.consecutive_losses = 0

    def register_loss(self, loss):

        self.daily_loss += abs(float(loss))
        self.consecutive_losses += 1

    def reset_daily(self):

        self.daily_loss = 0.0
        self.consecutive_losses = 0