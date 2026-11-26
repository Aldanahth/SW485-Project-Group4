"""Preprocessing used by rf_pipeline.joblib.

StudentPreprocessor repeats the exact steps of Phase1_Data_Exploration.ipynb
(drop 2nd-semester columns, add academic_progress and no_units_enrolled,
group rare categories, one-hot encode, standard-scale numeric columns), so the
pipeline can take a RAW student record (same columns as Dataset/data.csv) and
produce the same 102 features the Phase 1 Random Forest was trained on.

Any code that loads rf_pipeline.joblib must be able to import this module as
`Supervised_Learning.rf_pipeline_utils` (run it from the repository root).
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CLASS_NAMES = ["Dropout", "Enrolled", "Graduate"]
TARGET_CODES = {"Dropout": 0, "Enrolled": 1, "Graduate": 2}

CATEGORY_COLS = [
    "Marital status", "Application mode", "Course", "Previous qualification",
    "Nacionality", "Mother's qualification", "Father's qualification",
    "Mother's occupation", "Father's occupation",
]

NUMERIC_COLS = [
    "Age at enrollment", "Admission grade", "Previous qualification (grade)",
    "Application order",
    "Curricular units 1st sem (credited)", "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)", "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)", "Curricular units 1st sem (without evaluations)",
    "Unemployment rate", "Inflation rate", "GDP",
]

ENGINEERED_COLS = ["academic_progress", "no_units_enrolled"]


def load_raw_data(path="Dataset/data.csv"):
    """Read the original dataset (semicolon separated) and clean the column names."""
    df = pd.read_csv(path, sep=";")
    df.columns = df.columns.str.strip()
    return df


def add_engineered_features(X):
    """Drop 2nd-semester columns and add academic_progress and no_units_enrolled."""
    X = X.copy()
    X.columns = X.columns.str.strip()
    X = X.drop(columns=[c for c in X.columns if "2nd sem" in c or c == "Target"])

    enrolled = X["Curricular units 1st sem (enrolled)"]
    approved = X["Curricular units 1st sem (approved)"]
    # Students with 0 enrolled units get 0 (same rule as Phase 1)
    X["academic_progress"] = (approved / enrolled.where(enrolled > 0)).fillna(0)
    X["no_units_enrolled"] = (enrolled == 0).astype(int)
    return X


class StudentPreprocessor(BaseEstimator, TransformerMixin):
    """Raw student records -> the 102 preprocessed Phase 1 features (as a DataFrame)."""

    def __init__(self, rare_threshold=0.01):
        self.rare_threshold = rare_threshold

    def _group_rare(self, X):
        X = X.copy()
        for col in CATEGORY_COLS:
            values = X[col].astype(int)
            X[col] = values.where(values.isin(self.frequent_categories_[col]), -1)
        return X

    def fit(self, X, y=None):
        X = add_engineered_features(X)
        self.input_columns_ = list(X.columns)

        # Rare categories: used by less than 1% of TRAINING students -> -1 ("Other")
        self.frequent_categories_ = {}
        for col in CATEGORY_COLS:
            share = X[col].astype(int).value_counts(normalize=True)
            self.frequent_categories_[col] = list(share[share >= self.rare_threshold].index)
        X = self._group_rare(X)

        self.encoder_ = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.encoder_.fit(X[CATEGORY_COLS])
        self.scaler_ = StandardScaler()
        self.scaler_.fit(X[NUMERIC_COLS])

        self.base_columns_ = [c for c in self.input_columns_ if c not in CATEGORY_COLS]
        self.feature_names_out_ = self.base_columns_ + list(
            self.encoder_.get_feature_names_out(CATEGORY_COLS)
        )
        return self

    def transform(self, X):
        X = add_engineered_features(X)
        missing = [c for c in self.input_columns_ if c not in X.columns]
        if missing:
            raise ValueError(f"Missing input columns: {missing}")
        X = self._group_rare(X[self.input_columns_])

        encoded = pd.DataFrame(
            self.encoder_.transform(X[CATEGORY_COLS]),
            columns=self.encoder_.get_feature_names_out(CATEGORY_COLS),
            index=X.index,
        )
        base = X[self.base_columns_].copy()
        base[NUMERIC_COLS] = self.scaler_.transform(X[NUMERIC_COLS])
        return pd.concat([base, encoded], axis=1)[self.feature_names_out_]

    def get_feature_names_out(self, input_features=None):
        return np.array(self.feature_names_out_, dtype=object)

def get_key_drivers(pipeline, top_n=10):
    """Top features the Random Forest relies on, with one-hot columns added back
    to their original feature (e.g. all Course_* columns -> Course)."""
    names = pipeline.named_steps["preprocess"].get_feature_names_out()
    importance = pd.Series(pipeline.named_steps["model"].feature_importances_, index=names)

    def original_feature(column):
        for cat in CATEGORY_COLS:
            if column.startswith(cat + "_"):
                return cat
        return column

    return importance.groupby(original_feature).sum().sort_values(ascending=False).head(top_n)

def load_rf_pipeline(path="Supervised_Learning/models/rf_pipeline.joblib"):
    """Load the saved pipeline (preprocessing + tuned Random Forest)."""
    import joblib
    return joblib.load(Path(path))
