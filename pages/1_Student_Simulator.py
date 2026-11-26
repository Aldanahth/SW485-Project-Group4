"""Student Simulator: what-if predictions with the Phase 1 Random Forest pipeline."""

import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Supervised_Learning.rf_pipeline_utils import (  # noqa: E402
    CATEGORY_COLS, CLASS_NAMES, TARGET_CODES, load_raw_data, load_rf_pipeline,
    get_key_drivers as compute_key_drivers,
)

PIPELINE_PATH = ROOT / "Supervised_Learning" / "models" / "rf_pipeline.joblib"
DATA_PATH = ROOT / "Dataset" / "data.csv"

GRADE = "Curricular units 1st sem (grade)"
ENROLLED = "Curricular units 1st sem (enrolled)"
APPROVED = "Curricular units 1st sem (approved)"
EVALUATIONS = "Curricular units 1st sem (evaluations)"
TUITION = "Tuition fees up to date"
SCHOLARSHIP = "Scholarship holder"
PASS_GRADE = 10.0  # Portuguese 0-20 scale; every student with approved units has a grade >= 9.8

CLASS_COLORS = {"Dropout": "#d62728", "Enrolled": "#ff7f0e", "Graduate": "#2ca02c"}

READABLE_NAMES = {
    "academic_progress": "Academic progress (approved / enrolled units)",
    APPROVED: "Approved units (1st sem)",
    GRADE: "GPA (1st sem grade)",
    TUITION: "Tuition fees up to date",
    EVALUATIONS: "Evaluations (1st sem)",
    ENROLLED: "Enrolled units (1st sem)",
    "Admission grade": "Admission grade",
    "Age at enrollment": "Age at enrollment",
    "Previous qualification (grade)": "Previous qualification grade",
    SCHOLARSHIP: "Scholarship holder",
    "no_units_enrolled": "No units enrolled",
}
SLIDER_FEATURES = {
    "academic_progress", APPROVED, GRADE, TUITION, SCHOLARSHIP, "no_units_enrolled",
}


# ---------------------------------------------------------------- data & model
@st.cache_resource
def get_pipeline():
    return load_rf_pipeline(PIPELINE_PATH)


@st.cache_data
def get_test_students():
    """Raw records of the 885 Phase 1 test students (never seen during training)."""
    raw = load_raw_data(DATA_PATH)
    y = raw["Target"].map(TARGET_CODES)
    _, test_index = train_test_split(
        raw.index, test_size=0.2, stratify=y, random_state=42
    )
    return raw.loc[sorted(test_index)]


@st.cache_data
def get_key_drivers(top_n=10):
    """Global Random Forest importance, with one-hot columns added back to their original feature."""
    grouped = compute_key_drivers(get_pipeline(), top_n)
    return pd.DataFrame({
        "Feature": [READABLE_NAMES.get(f, f) for f in grouped.index],
        "Importance": grouped.values,
        "Controlled on this page": ["Yes" if f in SLIDER_FEATURES else "No" for f in grouped.index],
    })


def points_change(new, old, suffix=""):
    """Change in percentage points, or None (no arrow) when nothing changed."""
    change = round((new - old) * 100)
    return None if change == 0 else f"{change:+d} pts{suffix}"


def predict(student_row):
    proba = get_pipeline().predict_proba(student_row.drop(columns="Target", errors="ignore"))[0]
    return pd.Series(proba, index=CLASS_NAMES)


# ---------------------------------------------------------------- page
st.set_page_config(page_title="Student Simulator", layout="wide")
st.title("Student Simulator")
st.caption(
    "Change a student's first-semester results and see how the Random Forest's predicted "
    "outcome changes. Predictions support advisors; they are not final decisions."
)

if not PIPELINE_PATH.exists():
    st.error("Model not found: run Phase2_RF_Pipeline.ipynb to create "
             "Supervised_Learning/models/rf_pipeline.joblib.")
    st.stop()

students = get_test_students()

# ---- 1. choose a starting student
st.sidebar.header("1. Choose a student")
outcome_filter = st.sidebar.selectbox("Actual outcome", ["All"] + CLASS_NAMES)
pool = students if outcome_filter == "All" else students[students["Target"] == outcome_filter]
student_id = st.sidebar.selectbox(
    "Student (test set)", pool.index.tolist(),
    format_func=lambda i: f"Student #{i} - actual: {students.loc[i, 'Target']}",
)
original = students.loc[[student_id]]
enrolled_units = int(original[ENROLLED].iloc[0])

# ---- 2. scenario inputs
st.sidebar.header("2. Change the scenario")
if st.sidebar.button("Reset to the student's real values"):
    for key in ("approved", "gpa", "tuition", "scholarship"):
        st.session_state.pop(f"{key}_{student_id}", None)

if enrolled_units == 0:
    st.sidebar.info("This student enrolled in 0 units in the 1st semester, "
                    "so GPA and academic progress cannot be changed.")
    approved_units, gpa = 0, 0.0
else:
    approved_units = st.sidebar.select_slider(
        "Academic progress (used instead of attendance)",
        options=list(range(enrolled_units + 1)),
        value=int(original[APPROVED].iloc[0]),
        format_func=lambda n: f"{n} of {enrolled_units} units passed ({n / enrolled_units:.0%})",
        key=f"approved_{student_id}",
        help="The dataset has no attendance column, so academic progress "
             "(approved / enrolled units) is used as the engagement measure.",
    )
    if approved_units == 0:
        st.sidebar.info("With 0 passed units the GPA is 0 (it averages passed units only).")
        gpa = 0.0
    else:
        real_gpa = float(original[GRADE].iloc[0])
        gpa = st.sidebar.slider(
            "1st semester GPA (0-20 scale)",
            min_value=PASS_GRADE, max_value=20.0, step=0.1,
            value=round(min(max(real_gpa, PASS_GRADE), 20.0), 1),
            key=f"gpa_{student_id}",
            help="Average grade of the passed units, so it starts at the pass mark of 10.",
        )

tuition = st.sidebar.toggle("Tuition fees up to date", value=bool(original[TUITION].iloc[0]),
                            key=f"tuition_{student_id}")
scholarship = st.sidebar.toggle("Scholarship holder", value=bool(original[SCHOLARSHIP].iloc[0]),
                                key=f"scholarship_{student_id}")

# Build the scenario as a RAW record; the pipeline recalculates academic_progress itself,
# so the model never receives inconsistent values.
scenario = original.copy()
scenario[APPROVED] = approved_units
scenario[GRADE] = gpa
scenario[EVALUATIONS] = max(int(original[EVALUATIONS].iloc[0]), approved_units)
scenario[TUITION] = int(tuition)
scenario[SCHOLARSHIP] = int(scholarship)

# ---- 3. predictions
before, after = predict(original), predict(scenario)
predicted = after.idxmax()
confidence = after.max()

col1, col2, col3 = st.columns(3)
col1.metric("Predicted outcome", predicted,
            delta=None if predicted == before.idxmax() else f"was {before.idxmax()}",
            delta_color="off")
col2.metric("Confidence", f"{confidence:.0%}",
            delta=points_change(confidence, before[predicted], " vs real values"))
col3.metric("Dropout risk", f"{after['Dropout']:.0%}",
            delta=points_change(after["Dropout"], before["Dropout"]),
            delta_color="inverse")

if predicted == "Enrolled":
    st.warning("Enrolled is the hardest outcome to predict (Random Forest F1 about 0.43 in Phase 1), "
               "so treat this prediction with extra caution.")
elif confidence < 0.5:
    st.info("Low confidence: no outcome has more than 50% probability.")

left, right = st.columns(2)

with left:
    st.subheader("Outcome probabilities")
    prob_df = pd.DataFrame({
        "Outcome": CLASS_NAMES * 2,
        "Probability": list(before.values) + list(after.values),
        "Scenario": ["Real values"] * 3 + ["Simulated"] * 3,
    })
    prob_chart = (
        alt.Chart(prob_df)
        .mark_bar()
        .encode(
            y=alt.Y("Outcome:N", sort=CLASS_NAMES, title=None),
            yOffset=alt.YOffset("Scenario:N", sort=["Real values", "Simulated"]),
            x=alt.X("Probability:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("Outcome:N", legend=None,
                            scale=alt.Scale(domain=CLASS_NAMES,
                                            range=[CLASS_COLORS[c] for c in CLASS_NAMES])),
            opacity=alt.Opacity("Scenario:N",
                                scale=alt.Scale(domain=["Real values", "Simulated"],
                                                range=[0.35, 1.0]),
                                legend=alt.Legend(orient="bottom", title=None)),
            tooltip=["Outcome", "Scenario", alt.Tooltip("Probability:Q", format=".1%")],
        )
        .properties(height=220)
    )
    st.altair_chart(prob_chart, use_container_width=True)

    changes = pd.DataFrame({
        "Input": ["Approved units", "Academic progress", "GPA", "Tuition up to date", "Scholarship"],
        "Real value": [
            int(original[APPROVED].iloc[0]),
            f"{int(original[APPROVED].iloc[0]) / enrolled_units:.0%}" if enrolled_units else "-",
            f"{float(original[GRADE].iloc[0]):.1f}",
            "Yes" if original[TUITION].iloc[0] else "No",
            "Yes" if original[SCHOLARSHIP].iloc[0] else "No",
        ],
        "Simulated": [
            approved_units,
            f"{approved_units / enrolled_units:.0%}" if enrolled_units else "-",
            f"{gpa:.1f}",
            "Yes" if tuition else "No",
            "Yes" if scholarship else "No",
        ],
    })
    st.dataframe(changes, hide_index=True, use_container_width=True)

with right:
    st.subheader("Key drivers")
    drivers = get_key_drivers()
    driver_chart = (
        alt.Chart(drivers)
        .mark_bar()
        .encode(
            x=alt.X("Importance:Q", title="Importance in the Random Forest"),
            y=alt.Y("Feature:N", sort="-x", title=None,
                    axis=alt.Axis(labelLimit=320, labelOverlap=False)),
            color=alt.Color("Controlled on this page:N",
                            scale=alt.Scale(domain=["Yes", "No"], range=["#2a78d6", "#b8b8b8"]),
                            legend=alt.Legend(orient="bottom")),
            tooltip=["Feature", alt.Tooltip("Importance:Q", format=".3f")],
        )
        .properties(height=alt.Step(30))
    )
    st.altair_chart(driver_chart, use_container_width=True)
    st.caption(
        "Top 10 features the model relies on across all students (one-hot categories are "
        "added back together). Importance shows how much the model uses a feature, not the "
        "direction of its effect, and it does not prove causation."
    )
