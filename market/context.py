from market.fvg import FairValueGap
from market.order_blocks import OrderBlocks
from market.premium_discount import PremiumDiscount
from market.liquidity_map import LiquidityMap
from market.trend import TrendFilter


class MarketContext:

    def __init__(self):

        self.trend = TrendFilter()

        self.fvg = FairValueGap()

        self.blocks = OrderBlocks()

        self.discount = PremiumDiscount()

        self.liquidity = LiquidityMap()

    def build(
        self,
        df,
    ):

        trend = self.trend.direction(df)

        gaps = self.fvg.detect(df)

        bull = self.blocks.bullish(df)

        bear = self.blocks.bearish(df)

        price = df.close.iloc[-1]

        zone = self.discount.zone(

            df.high.tail(40).max(),

            df.low.tail(40).min(),

            price,
        )

        return {

            "trend": trend,

            "price": price,

            "nearest_gap": self.fvg.nearest(
                price,
                gaps,
            ),

            "bullish_ob": bull,

            "bearish_ob": bear,

            "premium_discount": zone,

            "equal_highs": self.liquidity.equal_highs(df),

            "equal_lows": self.liquidity.equal_lows(df),
        }