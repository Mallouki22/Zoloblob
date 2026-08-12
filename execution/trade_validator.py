from strategy.filter import TradeFilter
from strategy.score import Score
from config.settings import (
    HIGH_CONFIDENCE,
    MAX_TRADES_PER_DIRECTION,
)
class TradeValidator:

    def __init__(
        self,
        position_manager,
        order_manager,
        risk_guard,
    ):

        self.position_manager = position_manager
        self.order_manager = order_manager
        self.risk_guard = risk_guard

        self.filter = TradeFilter()
        self.score = Score()
    def check(
        self,
        prediction,
        symbol,
        account,
    ):

        symbol_info = self.order_manager.client.symbol_info(symbol)

        allowed, reason = self.risk_guard.refresh(
            self.order_manager.client,
            account.balance,
        )

        if not allowed:
            return False, reason

        signal = prediction["signal"]

        count = self.position_manager.count_direction(
            symbol,
            signal,
        )

        if count >= MAX_TRADES_PER_DIRECTION:

            if prediction["confidence"] < HIGH_CONFIDENCE:

                return (
                    False,
                    "Même direction déjà ouverte",
                )

        allowed, reason = self.filter.check(
            prediction,
            symbol_info,
            self.position_manager,
            symbol,
        )

        if not allowed:
            return False, reason

        result = self.score.calculate(
            prediction,
            symbol,
        )

        prediction["score"] = result["score"]

        print("\n===== SCORE =====")
        print("Score :", result["score"])
        print("Reason :", result["reason"])

        if not result["allow"]:
            return False, result["reason"]

        return True, "OK"