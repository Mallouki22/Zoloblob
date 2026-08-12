from execution.orders import OrderManager

manager = OrderManager()

symbol = manager.client.find_symbol("XAUUSD")

print("Symbole :", symbol)

entry = manager.client.symbol_tick(symbol).ask

print("Prix :", entry)

sl = entry - 10

tp = entry + 20

print("SL :", sl)

print("TP :", tp)

result = manager.buy(
    symbol=symbol,
    volume=0.01,
    sl=sl,
    tp=tp
)

print(result)