import joblib
import numpy as np

from ml.dataset import TradingDataset


def main():

    dataset = TradingDataset(
        "datasets/XAUUSD_ML_100k.parquet"
    )

    _, X_test, _, _ = dataset.prepare()

    model = joblib.load(
        "models/xgboost_gold.pkl"
    )

    predictions = model.predict(
        X_test
    )

    proba = model.predict_proba(
        X_test
    )

    confidence = np.max(
        proba,
        axis=1
    )

    print("\n===== PREDICTIONS =====")

    print(
        "Confidence moyenne :",
        round(confidence.mean(), 4)
    )

    print(
        "Confidence max :",
        round(confidence.max(), 4)
    )

    print(
        "Confidence min :",
        round(confidence.min(), 4)
    )

    print()

    print(
        "SELL :",
        np.sum(predictions == 0)
    )

    print(
        "WAIT :",
        np.sum(predictions == 1)
    )

    print(
        "BUY :",
        np.sum(predictions == 2)
    )


if __name__ == "__main__":
    main()