from market.trend import TrendFilter
from strategy.market_structure import MarketStructure
from strategy.bos import BOS
from strategy.liquidity import LiquiditySweep
from strategy.dxy_filter import DXYFilter
from market.htf import HTFTrend
from config.settings import (
    MIN_SCORE,
    TREND_SCORE,
    HTF_SCORE,
    MARKET_STRUCTURE_SCORE,
    BOS_SCORE,
    LIQUIDITY_SCORE,
    DXY_SCORE,
    ATR_SCORE,
    ADX_SCORE,
    CHOP_SCORE,
    USE_ADX_FILTER,
    USE_CHOP_FILTER,
    MIN_ADX,
    MAX_CHOP,
)
from market.volatility import VolatilityFilter
from market.atr_regime import ATRRegime
from market.adx_filter import ADXFilter
from market.chop_filter import ChopFilter


class Score:
    def __init__(self):
        self.trend = TrendFilter()
        self.market = MarketStructure()
        self.bos = BOS()
        self.liquidity = LiquiditySweep()
        self.dxy = DXYFilter()
        self.htf = HTFTrend()
        self.atr = ATRRegime()
        self.volatility = VolatilityFilter()
        self.adx = ADXFilter(MIN_ADX)
        self.chop = ChopFilter(MAX_CHOP)

    def calculate(self, prediction, symbol):
        signal = prediction["signal"]
        market = prediction["market"]

        score = 0
        reasons = []

        if USE_ADX_FILTER:
            if self.adx.allow(market):
                score += ADX_SCORE
            else:
                reasons.append("ADX")

        if USE_CHOP_FILTER:
            if self.chop.allow(market):
                score += CHOP_SCORE
            else:
                reasons.append("CHOP")

        if not self.volatility.allow(market):
            return {
                "score": 0,
                "allow": False,
                "reason": "Volatility",
                "atr_score": 0,
            }

        if self.trend.validate(signal, market):
            score += TREND_SCORE
        else:
            reasons.append("Trend")

        if self.htf.validate(symbol, signal):
            score += HTF_SCORE
        else:
            reasons.append("HTF")

        atr_score = self.atr.score(market)
        score += atr_score

        if atr_score == 0:
            reasons.append("ATR")

        if self.market.allow(market, signal):
            score += MARKET_STRUCTURE_SCORE
        else:
            reasons.append("Market Structure")

        if self.bos.allow(market, signal):
            score += BOS_SCORE
        else:
            reasons.append("BOS")

        if self.liquidity.allow(market, signal):
            score += LIQUIDITY_SCORE
        else:
            reasons.append("Liquidity")

        if self.dxy.allow(signal):
            score += DXY_SCORE
        else:
            reasons.append("DXY")

        return {
            "score": score,
            "allow": score >= MIN_SCORE,
            "reason": ", ".join(reasons) if reasons else "OK",
            "atr_score": atr_score,
        }