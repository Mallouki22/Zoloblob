import joblib
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

from config.settings import MODEL_PATH, DATASET_PATH
from ml.dataset import TradingDataset
from features.schema import model_input


def main():

    dataset = TradingDataset(DATASET_PATH)

    _, test_frame = dataset.split_frame()

    artifact = joblib.load(MODEL_PATH)

    ensemble = artifact["ensemble"]
    features = artifact["features"]

    X = model_input(
        test_frame,
        expected_columns=features,
    )

    y = test_frame["target"].astype(int).to_numpy()

    proba = ensemble.predict_proba(X)
    pred = np.argmax(proba, axis=1)
    conf = np.max(proba, axis=1)

    print("\n===== CONFUSION MATRIX =====")
    print(
        confusion_matrix(
            y,
            pred,
            labels=[0, 1, 2],
        )
    )

    print("\n===== CLASSIFICATION REPORT =====")
    print(
        classification_report(
            y,
            pred,
            labels=[0, 1, 2],
            target_names=["SELL", "WAIT", "BUY"],
            digits=4,
            zero_division=0,
        )
    )

    print("\n===== PREDICTIONS =====")
    for cls in [0, 1, 2]:
        print(
            cls,
            int((pred == cls).sum()),
            f"{(pred == cls).mean()*100:.2f}%"
        )

    print("\n===== CONFIDENCE =====")
    print("mean:", conf.mean())
    print("median:", np.median(conf))
    print("max:", conf.max())

    print("\n===== PROBABILITIES MEAN =====")
    print("SELL:", proba[:, 0].mean())
    print("WAIT:", proba[:, 1].mean())
    print("BUY :", proba[:, 2].mean())

    print("\n===== CONFIDENCE BY PREDICTED CLASS =====")

    for cls, name in [(0, "SELL"), (1, "WAIT"), (2, "BUY")]:
        mask = pred == cls

        if mask.any():
            print(
                name,
                "count=", mask.sum(),
                "confidence=",
                round(conf[mask].mean(), 4),
                "precision=",
                round((y[mask] == cls).mean(), 4),
            )


if __name__ == "__main__":
    main()