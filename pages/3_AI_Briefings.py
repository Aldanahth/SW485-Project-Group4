"""At-risk students list + AI advising briefing for the selected student."""
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "Generative_AI"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from dashboard_utils import CLASS_NAMES, RISK_THRESHOLD, load_scored_test_students, sidebar_filters  # noqa: E402
from dashboard_utils import get_pipeline  # noqa: E402
from Supervised_Learning.rf_pipeline_utils import get_key_drivers  # noqa: E402

# Use Aldana's real function when it exists; otherwise a placeholder with the same signature.
try:
    from genai_utils import generate_briefing
    PLACEHOLDER = False
except ImportError:
    PLACEHOLDER = True

    def generate_briefing(student, prediction, probs, top_features, cluster_profile, template):
        return (f"[Placeholder briefing] Predicted outcome: {prediction} "
                f"(Dropout probability {probs['Dropout']:.0%}). The real text arrives with genai_utils.py.")

st.set_page_config(page_title="AI Advising Briefings", page_icon="🧠", layout="wide")
st.title("🧠 AI Advising Briefings")
if PLACEHOLDER:
    st.warning("Using a placeholder: Generative_AI/genai_utils.py has not been pushed yet.")

students = sidebar_filters(load_scored_test_students())
at_risk = students[students["At risk"]].sort_values("P(Dropout)", ascending=False)

st.subheader(f"Students at risk ({len(at_risk)})")
st.caption(f"Test-set students with predicted Dropout probability ≥ {RISK_THRESHOLD:.0%}, highest risk first.")

table = at_risk[["Course name", "Age at enrollment", "Tuition up to date", "Scholarship",
                 "Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)", "P(Dropout)"]]
table = table.rename(columns={
    "Curricular units 1st sem (approved)": "Units approved",
    "Curricular units 1st sem (grade)": "1st sem grade",
    "P(Dropout)": "Dropout risk",
})
table["Dropout risk"] = table["Dropout risk"] * 100
table.index.name = "Student ID"
st.dataframe(table, use_container_width=True, column_config={
    "Dropout risk": st.column_config.ProgressColumn(format="%.0f%%", min_value=0, max_value=100),
})

if at_risk.empty:
    st.stop()

# ---- Briefing for one student ---------------------------------------------
st.subheader("Generate a briefing")
sid = st.selectbox("Student ID", at_risk.index)
row = at_risk.loc[sid]
probs = {name: float(row[f"P({name})"]) for name in CLASS_NAMES}

# Call the API only on click, and keep the result so it survives reruns.
if "briefings" not in st.session_state:
    st.session_state.briefings = {}

# Top 5 drivers, with this student's own value for each one
drivers = get_key_drivers(get_pipeline(), top_n=5)
enrolled = row["Curricular units 1st sem (enrolled)"]
student_values = row.to_dict()
student_values["academic_progress"] = (
    row["Curricular units 1st sem (approved)"] / enrolled if enrolled else 0
)
top_features = {feature: student_values.get(feature) for feature in drivers.index}

if st.button("Generate briefing", type="primary"):
    with st.spinner("Writing briefing..."):
        st.session_state.briefings[sid] = generate_briefing(
            student=row.to_dict(),
            prediction=row["Predicted"],
            probs=probs,
            top_features=top_features,
            cluster_profile=None,   # TODO: from cluster_profiles.json after Najd pushes
            template="T1",          # TODO: final template chosen by Sarah
        )

if sid in st.session_state.briefings:
    st.markdown(st.session_state.briefings[sid])
    st.caption("AI-generated. An advisor should review it before acting on it.")
