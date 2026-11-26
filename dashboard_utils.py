"""Shared loaders, labels and filters for the dashboard pages (app.py and pages/).

Reuses Aryam's Supervised_Learning/rf_pipeline_utils.py so every page reads the
data and the model the same way. Run the app from the repo root:
    streamlit run app.py
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent  # this file sits in the repo root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Supervised_Learning.rf_pipeline_utils import (  # noqa: E402
    CLASS_NAMES, TARGET_CODES, load_raw_data, load_rf_pipeline,
)

DATA_PATH = ROOT / "Dataset" / "data.csv"
PIPELINE_PATH = ROOT / "Supervised_Learning" / "models" / "rf_pipeline.joblib"
METRICS_PATH = ROOT / "Supervised_Learning" / "evaluation_results" / "test_metrics_summary.csv"
CLUSTER_MODEL_PATH = ROOT / "Unsupervised_Learning" / "outputs" / "cluster_model.joblib"
CLUSTER_PROFILES_PATH = ROOT / "Unsupervised_Learning" / "outputs" / "cluster_profiles.json"

# A student is flagged "at risk" when the predicted Dropout probability is at least this value.
RISK_THRESHOLD = 0.5
CLASS_COLORS = {"Dropout": "#d62728", "Enrolled": "#ff7f0e", "Graduate": "#2ca02c"}

# Course codes from the UCI dataset documentation.
COURSE_NAMES = {
    33: "Biofuel Production Technologies", 171: "Animation and Multimedia Design",
    8014: "Social Service (evening)", 9003: "Agronomy", 9070: "Communication Design",
    9085: "Veterinary Nursing", 9119: "Informatics Engineering", 9130: "Equinculture",
    9147: "Management", 9238: "Social Service", 9254: "Tourism", 9500: "Nursing",
    9556: "Oral Hygiene", 9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication", 9853: "Basic Education", 9991: "Management (evening)",
}
YES_NO = {1: "Yes", 0: "No"}
GENDER = {1: "Male", 0: "Female"}


def add_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Readable copies of coded columns (the original numeric columns stay for the model)."""
    df = df.copy()
    df["Course name"] = df["Course"].map(COURSE_NAMES).fillna("Other")
    df["Scholarship"] = df["Scholarship holder"].map(YES_NO)
    df["Tuition up to date"] = df["Tuition fees up to date"].map(YES_NO)
    df["Gender label"] = df["Gender"].map(GENDER)
    return df


@st.cache_data
def load_students() -> pd.DataFrame:
    """All 4,424 students (raw columns + readable labels)."""
    return add_labels(load_raw_data(DATA_PATH))


@st.cache_resource
def get_pipeline():
    return load_rf_pipeline(PIPELINE_PATH)


@st.cache_data
def load_test_metrics() -> pd.DataFrame:
    return pd.read_csv(METRICS_PATH, index_col=0)


@st.cache_data
def load_scored_test_students() -> pd.DataFrame:
    """The 885 Phase 1 test students, scored live by rf_pipeline.

    Same split as Phase 1 and the Student Simulator (80/20, stratified, random_state=42),
    so the model is never shown students it was trained on.
    """
    students = load_students()
    y = students["Target"].map(TARGET_CODES)
    _, test_index = train_test_split(students.index, test_size=0.2, stratify=y, random_state=42)
    test = students.loc[sorted(test_index)]

    raw_columns = [c for c in load_raw_data(DATA_PATH).columns if c != "Target"]
    probs = get_pipeline().predict_proba(test[raw_columns])
    for i, name in enumerate(CLASS_NAMES):
        test[f"P({name})"] = probs[:, i]
    test["Predicted"] = [CLASS_NAMES[i] for i in probs.argmax(axis=1)]
    test["Confidence"] = probs.max(axis=1)
    test["At risk"] = test["P(Dropout)"] >= RISK_THRESHOLD
    return test


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Same sidebar filters on every page; returns only the matching rows."""
    st.sidebar.header("Filters")
    courses = st.sidebar.multiselect("Course", sorted(df["Course name"].unique()))
    scholarship = st.sidebar.selectbox("Scholarship holder", ["All", "Yes", "No"])
    tuition = st.sidebar.selectbox("Tuition up to date", ["All", "Yes", "No"])
    gender = st.sidebar.selectbox("Gender", ["All", "Female", "Male"])

    mask = pd.Series(True, index=df.index)
    if courses:
        mask &= df["Course name"].isin(courses)
    if scholarship != "All":
        mask &= df["Scholarship"] == scholarship
    if tuition != "All":
        mask &= df["Tuition up to date"] == tuition
    if gender != "All":
        mask &= df["Gender label"] == gender
    return df[mask]
