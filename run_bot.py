from bot.trading_engine import TradingEngine

from execution.orders import OrderManager
from strategy.risk import RiskManager
from ml.predictor import Predictor


def main():

    predictor = Predictor()

    order_manager = OrderManager()

    account = order_manager.client.account_info()
    if account is None:
        raise RuntimeError("Impossible de récupérer le compte MT5.")

    risk_manager = RiskManager(
        capital=account.balance,
        risk=0.01
    )

    engine = TradingEngine(
        predictor=predictor,
        order_manager=order_manager,
        risk_manager=risk_manager
    )

    engine.start()


if __name__ == "__main__":
    main()