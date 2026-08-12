from data.pipeline import DataPipeline
from strategy.liquidity import LiquiditySweep

df = DataPipeline().run(bars=300)

liq = LiquiditySweep()

print(liq.direction(df))

print(liq.allow(df, "BUY"))

print(liq.allow(df, "SELL"))