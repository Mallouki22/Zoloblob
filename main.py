from ml.dataset import TradingDataset



def main():

    dataset = TradingDataset(
        "datasets/XAUUSD_15_100k.parquet"
    )


    X_train, X_test, y_train, y_test = (
        dataset.prepare()
    )


    print("TRAIN")
    print(X_train.shape)


    print("\nTEST")
    print(X_test.shape)


    print("\nClasses TRAIN")
    print(y_train.value_counts())


    print("\nClasses TEST")
    print(y_test.value_counts())



if __name__ == "__main__":
    main()