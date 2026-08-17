"""Feature-column contract for the ML model."""

from __future__ import annotations


EXCLUDED_FEATURES = {
    "setup_score",
}


def model_input(df, expected_columns=None):

    frame = df.drop(
        columns=[
            "time",
            "target",
            *EXCLUDED_FEATURES,
        ],
        errors="ignore",
    )

    if expected_columns is None:
        return frame

    expected = list(expected_columns)

    missing = [
        column
        for column in expected
        if column not in frame.columns
    ]

    unexpected = [
        column
        for column in frame.columns
        if column not in expected
    ]

    if missing or unexpected:

        details = []

        if missing:
            details.append(
                f"missing={missing}"
            )

        if unexpected:
            details.append(
                f"unexpected={unexpected}"
            )

        raise ValueError(
            "Feature contract mismatch: "
            + "; ".join(details)
        )

    return frame.loc[:, expected]