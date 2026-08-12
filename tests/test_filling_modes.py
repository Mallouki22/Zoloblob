import MetaTrader5 as mt5

from execution.orders import OrderManager

manager = OrderManager()

symbol = manager.client.find_symbol("XAUUSD")

tick = manager.client.symbol_tick(symbol)

price = tick.ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": 0.01,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 10,
    "tp": price + 20,
    "deviation": 20,
    "magic": 20260717,
    "comment": "TEST",
    "type_time": mt5.ORDER_TIME_GTC,
}

modes = {
    "FOK": mt5.ORDER_FILLING_FOK,
    "IOC": mt5.ORDER_FILLING_IOC,
    "RETURN": mt5.ORDER_FILLING_RETURN,
}

for name, mode in modes.items():

    request["type_filling"] = mode

    print("\n====================")
    print(name)

    result = mt5.order_send(request)

    print(result.retcode)
    print(result.comment)