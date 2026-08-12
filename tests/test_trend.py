from data.pipeline import DataPipeline
from market.trend import TrendFilter


def main():

    pipeline = DataPipeline()

    df = pipeline.run(
        bars=300
    )

    trend = TrendFilter()

    print(trend.direction(df))

    print(trend.validate("BUY", df))

    print(trend.validate("SELL", df))


if __name__ == "__main__":

    main()