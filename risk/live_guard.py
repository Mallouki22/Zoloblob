"""Synchronise les protections de risque avec les clôtures MT5."""

from __future__ import annotations

from datetime import datetime, time

import MetaTrader5 as mt5

from risk.guard import RiskGuard


class LiveRiskGuard(RiskGuard):
    def __init__(self, *args, magic_number: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.magic_number = magic_number
        self.processed_deals: set[int] = set()

    def refresh(self, client, balance: float) -> tuple[bool, str]:
        self.reset_if_new_day(balance)
        start = datetime.combine(self.day, time.min)
        deals = mt5.history_deals_get(start, datetime.now()) or []
        exit_entries = {mt5.DEAL_ENTRY_OUT, mt5.DEAL_ENTRY_OUT_BY}
        for deal in deals:
            if deal.ticket in self.processed_deals:
                continue
            if deal.magic != self.magic_number or deal.entry not in exit_entries:
                continue
            self.processed_deals.add(deal.ticket)
            self.record_closed_trade(deal.profit + deal.swap + deal.commission)
        return self.can_open(balance)
