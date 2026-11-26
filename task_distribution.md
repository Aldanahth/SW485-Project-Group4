# Phase 2 Task Distribution

## Team Responsibilities

| Member | Area | Responsibilities | Deadline |
|---|---|---|---|
| Najd | Unsupervised Learning (Algorithm 1) | Clustering rationale; data preparation (drop `Target`); choosing k (Elbow + Silhouette); K-Means; describing each cluster; saving `cluster_profiles.json` and `cluster_model.joblib`; testing the cluster label as an extra feature for Random Forest | 26 Nov |
| Yusra | Unsupervised Learning (Algorithm 2 and comparison) | Second algorithm (Agglomerative or GMM); comparison table (Silhouette, Davies-Bouldin, WCSS, BCubed); all cluster plots (PCA/t-SNE, cluster sizes, feature means); Integration Strategy and Challenges sections | 28 Nov |
| Aldana | Generative AI (setup and templates) | API setup with the key stored securely in `.env`; `genai_utils.py`; designing and documenting the two prompt templates; `prompt_design_rationale.md` (except Lessons Learned) | 27 Nov |
| Sarah | Generative AI (evaluation) | Test cases (at least 3 per template); quantitative metrics (length, keywords, Flesch-Kincaid, preference rating); qualitative evaluation; selecting the best template; ethics; Integration Plan; Lessons Learned section | 30 Nov |
| Aryam | Dashboard (model pipeline and simulator) | `rf_pipeline.joblib` (preprocessing + Random Forest, verified to match Phase 1 results); `pages/1_Student_Simulator.py` (GPA and attendance sliders, prediction with confidence, key-drivers chart); `task_distribution.md` | Pipeline: 25 Nov; Page: 1 Dec |
| Jumana | Dashboard (main app and deployment) | `app.py` (cohort retention KPI cards); `pages/2_Cohort_Clusters.py`; AI advising-briefings panel for at-risk students; deployment on Streamlit Cloud; updating the README with the app link | 1 Dec |

## Shared Files (names must not be changed)

| File | Produced by | Used by |
|---|---|---|
| `Unsupervised_Learning/outputs/cluster_profiles.json` | Najd | Aldana, Sarah, Jumana |
| `Unsupervised_Learning/outputs/cluster_model.joblib` | Najd | Jumana |
| `Supervised_Learning/models/rf_pipeline.joblib` | Aryam | Jumana, Aldana, Sarah |
| `Generative_AI/genai_utils.py` with `generate_briefing(student, prediction, probs, top_features, cluster_profile, template)` | Aldana | Sarah, Jumana |

If a member needs a file that is not finished yet, they use a temporary placeholder with the same name and format, then replace it when the final version is delivered.

## Notebook Order

- **Clustering notebook:** Najd first, then Yusra.
- **Generative AI notebook:** Aldana first, then Sarah.

## Timeline

| Date | Deliverable |
|---|---|
| 25 Nov | `rf_pipeline.joblib` (Aryam) |
| 26 Nov | K-Means, cluster profiles and cluster model (Najd) |
| 27 Nov | `genai_utils.py`, templates, prompt design rationale (Aldana) |
| 28 Nov | Second clustering algorithm, comparison and plots (Yusra) |
| 30 Nov | GenAI evaluation, ethics, Integration Plan (Sarah) |
| 1 Dec | Student Simulator page (Aryam); main app, Cohort Clusters page, deployment (Jumana) |
