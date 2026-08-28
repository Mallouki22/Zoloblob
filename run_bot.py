import joblib

from bot.trading_engine import TradingEngine
from execution.orders import OrderManager
from strategy.risk import RiskManager
from ml.predictor import Predictor


MODEL_PATH = "models/xgboost_gold.pkl"


def main():

    # =========================
    # LOAD MODEL
    # =========================

    artifact = joblib.load(MODEL_PATH)

    if not isinstance(artifact, dict):
        raise TypeError(
            "Model artifact invalide : dict attendu."
        )

    ensemble = artifact["ensemble"]

    predictor = Predictor(
        model=ensemble
    )

    # =========================
    # MT5 / ORDER / RISK
    # =========================

    order_manager = OrderManager()

    risk_manager = RiskManager()

    # =========================
    # TRADING ENGINE
    # =========================

    engine = TradingEngine(
        predictor=predictor,
        order_manager=order_manager,
        risk_manager=risk_manager,
    )

    engine.start()


if __name__ == "__main__":
    main()