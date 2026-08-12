import unittest

import pandas as pd

from backtest.engine import BacktestEngine
from risk.guard import RiskGuard


class BacktestEngineTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame({
            "time": pd.date_range("2026-01-01", periods=4, freq="15min"),
            "open": [100.0, 100.0, 100.0, 100.0],
            "high": [101.0, 101.0, 101.0, 105.0],
            "low": [99.0, 99.0, 97.0, 99.0],
            "close": [100.0, 100.0, 99.0, 104.0],
            "ATR": [1.0, 1.0, 1.0, 1.0],
            "spread": [20, 20, 20, 20],
        })

    def test_signal_executes_on_next_candle_and_stop_is_conservative(self):
        engine = BacktestEngine(
            self.frame, [2, 1, 2, 1], [0.8] * 4,
            capital=10_000, point_size=0.01, slippage_points=0,
        )
        trades = engine.run()
        self.assertEqual(len(trades), 2)
        self.assertEqual(trades.iloc[0]["exit_reason"], "STOP")
        self.assertEqual(trades.iloc[1]["exit_reason"], "TARGET")
        self.assertEqual(engine.rejections["Signal WAIT"], 1)

    def test_daily_loss_guard_blocks_new_entries(self):
        guard = RiskGuard(max_daily_loss=0.01, max_consecutive_losses=3)
        guard.reset_if_new_day(100.0)
        guard.record_closed_trade(-2.0)
        allowed, _ = guard.can_open(98.0)
        self.assertFalse(allowed)
