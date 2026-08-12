"""Deterministic setup-quality feature used in every pipeline."""

from __future__ import annotations


class SetupDetector:
    def __init__(self, df):
        self.df = df.copy()

    def compute_score(self):
        scores = []
        for _, row in self.df.iterrows():
            score = 0
            if row["EMA_20"] > row["EMA_50"]:
                score += 15
            if row["ADX_14"] > 25:
                score += 15
            if 55 <= row["RSI"] <= 70:
                score += 10
            if row["MACD_12_26_9"] > 0:
                score += 10
            if row["ATR_percent"] > 0.0015:
                score += 10
            if 0.20 <= row["BB_position"] <= 0.80:
                score += 10
            if abs(row["body"]) > row["range"] * 0.6:
                score += 15
            if row["upper_wick"] < row["body"] * 0.5:
                score += 5
            if row["lower_wick"] < row["body"] * 0.5:
                score += 5
            if abs(row["EMA20_distance"]) > 0.001:
                score += 5
            scores.append(score)
        self.df["setup_score"] = scores
        return self.df
