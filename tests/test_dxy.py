from strategy.dxy_filter import DXYFilter


dxy = DXYFilter()

print(dxy.get_trend())
print(dxy.allow("BUY"))
print(dxy.allow("SELL"))