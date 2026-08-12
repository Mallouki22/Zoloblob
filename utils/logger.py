"""
Trading Logger
"""

from pathlib import Path
from datetime import datetime
import csv


class TradingLogger:

    def __init__(self):

        Path("logs").mkdir(exist_ok=True)

        self.file = "logs/trades.csv"

        if not Path(self.file).exists():

            with open(
                self.file,
                "w",
                newline="",
                encoding="utf-8",
            ) as f:

                writer = csv.writer(f)

                writer.writerow([
                    "datetime",
                    "symbol",
                    "signal",
                    "confidence",
                    "score",
                    "entry",
                    "sl",
                    "tp1",
                    "tp2",
                    "tp3",
                    "risk",
                    "lot",
                    "status",
                ])

    def log(
        self,
        symbol,
        prediction,
        entry,
        sl,
        tp,
        lot,
        status,
    ):

        with open(
            self.file,
            "a",
            newline="",
            encoding="utf-8",
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now(),
                symbol,
                prediction["signal"],
                round(prediction["confidence"], 3),
                prediction.get("score", 0),
                entry,
                sl,
                prediction.get("tp1"),
                prediction.get("tp2"),
                prediction.get("tp3"),
                prediction.get("risk"),
                lot,
                status,
            ])