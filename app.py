"""Home page: cohort retention KPIs for decision-makers.

Run from the repo root:  streamlit run app.py
"""
import altair as alt
import streamlit as st

from dashboard_utils import (
    CLASS_COLORS, CLASS_NAMES, PIPELINE_PATH, RISK_THRESHOLD,
    load_scored_test_students, load_students, load_test_metrics, sidebar_filters,
)

st.set_page_config(page_title="Student Retention Dashboard", page_icon="🎓", layout="wide")
st.title("🎓 Student Retention & Advisory Dashboard")
st.caption("Early-warning view after the 1st semester. Use the filters on the left to focus on a group.")

students = load_students()
filtered = sidebar_filters(students)
if filtered.empty:
    st.warning("No students match these filters.")
    st.stop()

# ---- Cohort KPIs: actual outcomes ------------------------------------------
st.subheader("Cohort outcomes")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Students", f"{len(filtered):,}")
k2.metric("Dropout rate", f"{(filtered['Target'] == 'Dropout').mean():.1%}")
k3.metric("Graduation rate", f"{(filtered['Target'] == 'Graduate').mean():.1%}")
k4.metric("Still enrolled", f"{(filtered['Target'] == 'Enrolled').mean():.1%}")

# ---- Early-warning KPIs: live model predictions on the test set ------------
st.subheader("Early-warning model")
if not PIPELINE_PATH.exists():
    st.error("Model not found: Supervised_Learning/models/rf_pipeline.joblib is missing.")
    st.stop()

test = load_scored_test_students()
test_f = test[test.index.isin(filtered.index)]
rf_acc = load_test_metrics().loc["Random Forest", "Accuracy"]

m1, m2, m3 = st.columns(3)
m1.metric("Students flagged at risk", f"{int(test_f['At risk'].sum())} / {len(test_f)}",
          help=f"Test-set students with predicted Dropout probability ≥ {RISK_THRESHOLD:.0%}.")
m2.metric("Model accuracy (all test students)", f"{rf_acc:.1%}",
          help="Random Forest accuracy on all 885 test students (Phase 1). It does not change with the filters.")
m3.metric("Average prediction confidence", f"{test_f['Confidence'].mean():.1%}" if len(test_f) else "–",
          help="Mean of the highest class probability for each student.")
st.caption("Predictions cover the 885 held-out test students only, so the model is never scored "
           "on students it was trained on.")

# ---- Charts -----------------------------------------------------------------
color_scale = alt.Scale(domain=CLASS_NAMES, range=[CLASS_COLORS[c] for c in CLASS_NAMES])
c1, c2 = st.columns(2)

with c1:
    st.markdown("**Outcome distribution**")
    counts = filtered["Target"].value_counts().reset_index()
    counts.columns = ["Outcome", "Students"]
    donut = (
        alt.Chart(counts).mark_arc(innerRadius=60)
        .encode(theta="Students:Q",
                color=alt.Color("Outcome:N", scale=color_scale, legend=alt.Legend(orient="bottom")),
                tooltip=["Outcome", "Students"])
        .properties(height=300)
    )
    st.altair_chart(donut, use_container_width=True)

with c2:
    factor = st.selectbox("Dropout rate by", ["Tuition up to date", "Scholarship", "Gender label", "Course name"])

    # For each group: dropout rate AND number of students
    rate = (filtered.groupby(factor)["Target"]
            .agg(**{"Dropout rate": lambda s: (s == "Dropout").mean(), "Students": "size"})
            .reset_index())

    # Small groups give unreliable rates, so they are hidden by default (the user can show them)
    MIN_GROUP = 10
    show_small = st.checkbox(f"Show groups with fewer than {MIN_GROUP} students", value=False)
    hidden = 0 if show_small else (rate["Students"] < MIN_GROUP).sum()
    if not show_small:
        rate = rate[rate["Students"] >= MIN_GROUP]

        if hidden:
           st.caption(f"{hidden} group(s) with fewer than {MIN_GROUP} students are hidden.")
    if show_small:
        st.caption(f"⚠️ Rates for groups with fewer than {MIN_GROUP} students are unreliable. "
                   "Hover over a bar to see how many students it represents.")

    if rate.empty:
        st.info("Not enough students in any group to show a reliable rate. "
                "Try fewer filters, or tick the box above to show small groups.")
    else:
        bars = (
            alt.Chart(rate).mark_bar(color=CLASS_COLORS["Dropout"])
            .encode(x=alt.X("Dropout rate:Q", axis=alt.Axis(format="%")),
                    y=alt.Y(f"{factor}:N", sort="-x", title=None, axis=alt.Axis(labelLimit=250)),
                    tooltip=[factor, alt.Tooltip("Dropout rate:Q", format=".1%"), "Students"])
            .properties(height=alt.Step(28))
        )
        st.altair_chart(bars, use_container_width=True)

st.info("These charts show associations in the data, not causes. Predictions support advisors; "
        "they are not final decisions.")
