"""
Premium Discount
"""


class PremiumDiscount:

    def zone(
        self,
        swing_high,
        swing_low,
        price,
    ):

        midpoint = (

            swing_high
            + swing_low

        ) / 2

        if price < midpoint:

            return "DISCOUNT"

        if price > midpoint:

            return "PREMIUM"

        return "EQUILIBRIUM"