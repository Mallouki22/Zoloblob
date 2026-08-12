import unittest

import pandas as pd

from features.schema import model_input


class ModelInputContractTests(unittest.TestCase):
    def test_orders_expected_features(self):
        frame = pd.DataFrame({"time": [1], "target": [2], "b": [2.0], "a": [1.0]})
        result = model_input(frame, ["a", "b"])
        self.assertEqual(list(result.columns), ["a", "b"])

    def test_rejects_feature_mismatch(self):
        frame = pd.DataFrame({"a": [1.0], "extra": [2.0]})
        with self.assertRaisesRegex(ValueError, "Feature contract mismatch"):
            model_input(frame, ["a", "b"])
