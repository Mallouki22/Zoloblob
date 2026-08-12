from data.pipeline import DataPipeline
from strategy.market_structure import MarketStructure

pipeline = DataPipeline()

df = pipeline.run(bars=300)

structure = MarketStructure()

print(structure.trend(df))

print(structure.allow(df, "BUY"))

print(structure.allow(df, "SELL"))