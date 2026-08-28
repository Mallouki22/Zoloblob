"""Shared feature contract used by dataset creation, backtests and live trading."""

from __future__ import annotations

import pandas as pd

from features.generator import FeatureGenerator
from features.processor import FeatureProcessor
from features.setup import SetupDetector
from features.market_structure_features import add_market_structure_features


class FeaturePipeline:
    """Builds the exact same feature set regardless of the caller."""

    def __init__(self, drop_na: bool = True):
        self.drop_na = drop_na

    def run(self, df: pd.DataFrame) -> pd.DataFrame:

        featured = FeatureGenerator(df).generate()

        featured = add_market_structure_features(
            featured
        )

        featured = FeatureProcessor(
            featured
        ).run(
            drop_na=self.drop_na
        )

        featured = SetupDetector(
            featured
        ).compute_score()

        return featured


def build_features(
    df: pd.DataFrame,
    drop_na: bool = True,
) -> pd.DataFrame:

    return FeaturePipeline(
        drop_na=drop_na
    ).run(df)