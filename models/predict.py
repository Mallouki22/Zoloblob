import joblib
import numpy as np

from ml.dataset import TradingDataset


def main():

    dataset = TradingDataset(
        "datasets/XAUUSD_ML_100k.parquet"
    )

    _, X_test, _, y_test = dataset.prepare()

    data = joblib.load(
        "models/xgboost_gold.pkl"
    )

    print("\n===== MODEL TYPE =====")
    print(type(data))

    if isinstance(data, dict):

        print("\n===== MODEL KEYS =====")
        print(data.keys())

        for key, value in data.items():
            print(
                f"{key}: {type(value)}"
            )

        model = None

        for key in [
            "model",
            "xgboost",
            "estimator",
            "classifier",
            "best_model",
        ]:

            if key in data and hasattr(
                data[key],
                "predict"
            ):
                model = data[key]
                break

        if model is None:

            for value in data.values():

                if hasattr(
                    value,
                    "predict"
                ):
                    model = value
                    break

        if model is None:
            raise TypeError(
                "Aucun objet modèle trouvé dans le dictionnaire."
            )

    else:

        model = data

    print("\n===== REAL MODEL =====")
    print(type(model))

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

    print("\n===== ACTUAL =====")

    print(
        "SELL :",
        np.sum(y_test == 0)
    )

    print(
        "WAIT :",
        np.sum(y_test == 1)
    )

    print(
        "BUY :",
        np.sum(y_test == 2)
    )


if __name__ == "__main__":
    main()
