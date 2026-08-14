"""
Dataset preparation for 3-class ML trading model.

Classes:
    0 = SELL
    1 = WAIT
    2 = BUY
"""

import pandas as pd

from features.schema import model_input


class TradingDataset:

    def __init__(self, path):
        self.path = path

    def load(self):
        return pd.read_parquet(self.path)

    def split_frame(self):
        df = self.load()

        split = int(len(df) * 0.8)

        return (
            df.iloc[:split].copy(),
            df.iloc[split:].copy(),
        )

    def prepare(self):

        df = self.load()

        print("\n===== COLONNES DATASET =====")
        print(df.columns.tolist())

        print("\n===== TYPES =====")
        print(df.dtypes)

        # ==========================
        # FEATURES
        # ==========================

        X = model_input(df)

        # ==========================
        # TARGET
        # ==========================

        y = df["target"].copy()

        print("\n===== TARGET ORIGINAL =====")
        print(y.value_counts(dropna=False).sort_index())

        # ==========================
        # VALID TARGETS
        # ==========================

        valid = y.isin([0, 1, 2])

        X = X.loc[valid].copy()
        y = y.loc[valid].copy()

        # ==========================
        # TEMPORAL SPLIT
        # ==========================

        split = int(len(X) * 0.8)

        X_train = X.iloc[:split].copy()
        X_test = X.iloc[split:].copy()

        y_train = y.iloc[:split].copy()
        y_test = y.iloc[split:].copy()

        # ==========================
        # REMOVE NaN TARGET
        # ==========================

        train_mask = y_train.notna()

        X_train = X_train.loc[train_mask]
        y_train = y_train.loc[train_mask].astype(int)

        test_mask = y_test.notna()

        X_test = X_test.loc[test_mask]
        y_test = y_test.loc[test_mask].astype(int)

        # ==========================
        # DEBUG
        # ==========================

        print("\n===== TARGET ML =====")

        print("\nTRAIN:")
        print(y_train.value_counts().sort_index())

        print("\nTEST:")
        print(y_test.value_counts().sort_index())

        print("\n===== CLASSES =====")
        print("Train:", sorted(y_train.unique()))
        print("Test :", sorted(y_test.unique()))

        print("\n===== FEATURES =====")
        print(X.columns.tolist())

        return (
            X_train,
            X_test,
            y_train,
            y_test,
        )