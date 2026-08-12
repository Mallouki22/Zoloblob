from mt5.client import MT5Client

client = MT5Client()

client.initialize()

for symbol in client.positions():
    pass

symbols = [
    s.name
    for s in __import__("MetaTrader5").symbols_get()
    if "XAUUSD" in s.name.upper()
]

print()

print("===== SYMBOLS =====")

for s in symbols:

    print(s)