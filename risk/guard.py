"""Stateful risk protections shared by live execution and simulation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class RiskGuard:
    max_daily_loss: float
    max_consecutive_losses: int
    day: date | None = None
    start_of_day_balance: float | None = None
    realised_today: float = 0.0
    consecutive_losses: int = 0

    def reset_if_new_day(self, balance: float, today: date | None = None) -> None:
        today = today or date.today()
        if self.day != today:
            self.day = today
            self.start_of_day_balance = balance
            self.realised_today = 0.0
            self.consecutive_losses = 0

    def record_closed_trade(self, pnl: float) -> None:
        self.realised_today += pnl
        self.consecutive_losses = self.consecutive_losses + 1 if pnl < 0 else 0

    def can_open(self, balance: float, today: date | None = None) -> tuple[bool, str]:
        self.reset_if_new_day(balance, today)
        assert self.start_of_day_balance is not None

        # Account balance is also checked so a broker-side closure is not
        # ignored when the process was restarted or did not observe it.
        day_pnl = min(self.realised_today, balance - self.start_of_day_balance)
        if day_pnl <= -(self.start_of_day_balance * self.max_daily_loss):
            return False, "Limite de perte journalière atteinte"
        if self.consecutive_losses >= self.max_consecutive_losses:
            return False, "Limite de pertes consécutives atteinte"
        return True, "OK"
