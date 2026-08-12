from data.pipeline import DataPipeline
from strategy.bos import BOS

df = DataPipeline().run(bars=300)

bos = BOS()

print(bos.direction(df))

print(bos.allow(df, "BUY"))

print(bos.allow(df, "SELL"))