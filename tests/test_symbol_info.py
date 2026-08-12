from mt5.client import MT5Client

client = MT5Client()
client.initialize()

symbol = client.find_symbol("XAUUSD")

info = client.symbol_info(symbol)

print("Symbol :", symbol)
print("trade_mode       :", info.trade_mode)
print("trade_exemode    :", info.trade_exemode)
print("filling_mode     :", info.filling_mode)
print("order_mode       :", info.order_mode)
print("volume_min       :", info.volume_min)
print("volume_step      :", info.volume_step)
print("volume_max       :", info.volume_max)