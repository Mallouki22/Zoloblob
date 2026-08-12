from execution.orders import OrderManager


def main():

    manager = OrderManager()

    symbol = manager.client.find_symbol("XAUUSD")

    print("Symbole :", symbol)

    result = manager.buy(

        symbol=symbol,

        volume=0.01,

        sl=3000,

        tp=4000

    )

    print(result)


if __name__ == "__main__":

    main()