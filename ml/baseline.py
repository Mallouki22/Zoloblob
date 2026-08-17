import pandas as pd

from config.settings import DATASET_PATH
from ml.dataset import TradingDataset


def main():

    dataset = TradingDataset(DATASET_PATH)

    X_train, X_test, y_train, y_test = dataset.prepare()

    df = pd.read_parquet(DATASET_PATH)

    split = int(len(df) * 0.8)

    test = df.iloc[split:].copy()

    # ==========================================
    # SIMPLE PRICE MOMENTUM BASELINES
    # ==========================================

    for lookback in [1, 3, 5, 10, 20]:

        momentum = test["close"].pct_change(lookback)

        prediction = pd.Series(
            1,
            index=test.index,
        )

        prediction[momentum > 0] = 2
        prediction[momentum < 0] = 0

        actual = test["target"]

        valid = momentum.notna()

        accuracy = (
            prediction[valid] == actual[valid]
        ).mean()

        print(
            f"Momentum {lookback:>2} : "
            f"{accuracy * 100:.2f}%"
        )

    # ==========================================
    # DIRECTIONAL BASELINE
    # SELL / BUY ONLY
    # ==========================================

    print("\n===== BASELINE DIRECTIONNELLE =====")

    for lookback in [1, 3, 5, 10, 20]:

        momentum = test["close"].pct_change(lookback)

        valid = momentum.notna()

        prediction = (momentum > 0).astype(int)

        # BUY = 2
        # SELL = 0

        pred_target = prediction.map({
            0: 0,
            1: 2,
        })

        directional = test["target"].isin([0, 2])

        valid = valid & directional

        accuracy = (
            pred_target[valid]
            == test.loc[valid, "target"]
        ).mean()

        print(
            f"Momentum {lookback:>2} "
            f"directional : "
            f"{accuracy * 100:.2f}%"
        )


if __name__ == "__main__":
    main()