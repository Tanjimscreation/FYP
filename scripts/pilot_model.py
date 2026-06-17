"""Run a preliminary NHANES depression classification pilot model."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
from sklearn.impute import SimpleImputer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "nhanes"
RESULTS_DIR = PROJECT_ROOT / "results"

PHQ_COLS = [
    "DPQ010",
    "DPQ020",
    "DPQ030",
    "DPQ040",
    "DPQ050",
    "DPQ060",
    "DPQ070",
    "DPQ080",
    "DPQ090",
]

TARGET = "DEPRESSION"
RANDOM_STATE = 42

warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"sklearn\..*")


def load_merged_nhanes() -> pd.DataFrame:
    demo, _ = pyreadstat.read_xport(DATA_DIR / "DEMO_J.XPT")
    dpq, _ = pyreadstat.read_xport(DATA_DIR / "DPQ_J.XPT")
    paq, _ = pyreadstat.read_xport(DATA_DIR / "PAQ_J.XPT")
    hoq, _ = pyreadstat.read_xport(DATA_DIR / "HOQ_J.XPT")

    return (
        demo.merge(dpq, on="SEQN", how="inner")
        .merge(paq, on="SEQN", how="inner")
        .merge(hoq, on="SEQN", how="inner")
    )


def add_depression_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["PHQ9_TOTAL"] = (
        df[PHQ_COLS].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=9)
    )
    df = df.dropna(subset=["PHQ9_TOTAL"]).copy()
    df[TARGET] = (df["PHQ9_TOTAL"] >= 10).astype(int)
    return df


def make_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    leakage_cols = set(PHQ_COLS + ["DPQ100", "PHQ9_TOTAL", TARGET])
    identifier_or_design_cols = {
        "SEQN",
        "SDDSRVYR",
        "WTINT2YR",
        "WTMEC2YR",
        "SDMVPSU",
        "SDMVSTRA",
    }
    exclude_cols = leakage_cols | identifier_or_design_cols

    feature_cols = [col for col in df.columns if col not in exclude_cols]
    X = df[feature_cols].apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan).astype(float)

    # Keep the pilot stable by dropping columns that are mostly unavailable.
    missing_fraction = X.isna().mean()
    X = X.loc[:, missing_fraction <= 0.80]

    # Drop constants after missing-heavy columns are removed.
    non_constant_cols = [col for col in X.columns if X[col].nunique(dropna=True) > 1]
    X = X[non_constant_cols]

    y = df[TARGET]
    return X, y


def run_pilot() -> dict[str, object]:
    df = add_depression_label(load_merged_nhanes())
    X, y = make_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "classifier",
                SGDClassifier(
                    loss="log_loss",
                    class_weight="balanced",
                    max_iter=5000,
                    tol=1e-4,
                    alpha=0.001,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_score = model.predict_proba(X_test)[:, 1]

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = tn / (tn + fp)

    metrics = {
        "model": "SGDClassifier(loss='log_loss', class_weight='balanced')",
        "random_state": RANDOM_STATE,
        "rows_total_valid_phq9": int(len(df)),
        "features_used": int(X.shape[1]),
        "positive_class_rate": float(y.mean()),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "auc_roc": float(roc_auc_score(y_test, y_score)),
        "f1": float(f1_score(y_test, y_pred)),
        "recall_sensitivity": float(recall_score(y_test, y_pred)),
        "specificity": float(specificity),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
        "feature_columns": list(X.columns),
    }
    return metrics


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics = run_pilot()

    metrics_path = RESULTS_DIR / "pilot_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n")

    print("Pilot model results")
    print(f"Rows with complete PHQ-9: {metrics['rows_total_valid_phq9']}")
    print(f"Features used: {metrics['features_used']}")
    print(f"Test rows: {metrics['test_rows']}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"AUC-ROC: {metrics['auc_roc']:.4f}")
    print(f"F1 score: {metrics['f1']:.4f}")
    print(f"Recall/Sensitivity: {metrics['recall_sensitivity']:.4f}")
    print(f"Specificity: {metrics['specificity']:.4f}")
    print(f"Confusion matrix: {metrics['confusion_matrix']}")
    print(f"Saved metrics to: {metrics_path}")


if __name__ == "__main__":
    main()
