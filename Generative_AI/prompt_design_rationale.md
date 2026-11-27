# Prompt Design Rationale

## 1. Overview

The University Student Retention & Advisory Dashboard uses Google Gemini 3.8 Flash to generate supportive academic guidance based on supervised learning predictions, available student features, and clustering profiles when available.

Two prompt templates were designed for different users: academic advisors and students. Both templates use the same structured input data but differ in their intended audience, tone, level of detail, and recommended actions.

## 2. Template 1: Advisor Briefing

**Template ID:** `advisor`

**Intended Use Case:** Generate a professional academic briefing to help university advisors understand a student's predicted academic status and identify suitable support interventions.

**Design Rationale:** Academic advisors need concise, evidence-based information to prioritize support. This template uses a structured, professional style and requests a summary of predicted status, relevant academic indicators, available cluster characteristics, and two to three practical interventions.

**Prompt Structure:** The template receives `{student}`, `{prediction}`, `{probs}`, `{top_features}`, and `{cluster_profile}`. It instructs Gemini to use only the provided evidence, distinguish predictions from facts, and avoid unsupported assumptions.

**Illustrative Example Input:**
- Predicted status: Dropout
- Dropout probability: 0.76
- Important factors: Low academic progress and tuition status not up to date
- Cluster profile: Students with academic and financial support needs

**Illustrative Example Output:**

"The model predicts an elevated risk of dropout, but this is not a confirmed outcome. Available records indicate limited academic progress and a tuition status that is not up to date. An academic advisor should review the student's academic progress, verify the tuition status with student services, and arrange a supportive follow-up meeting. These indicators do not establish the causes of the prediction."

**Assumptions and Limitations:**
- Model predictions may be incorrect.
- Global feature importance describes overall model behavior and does not explain an individual student's prediction or establish causation.
- Cluster descriptions represent generalized group patterns, not individual diagnoses.
- Missing information must not be inferred or invented.
- Recommendations require human review before action.

## 3. Template 2: Student Outreach

**Template ID:** `student`

**Intended Use Case:** Generate a supportive outreach message that encourages a student to seek academic assistance.

**Design Rationale:** Student-facing communication should be understandable, respectful, and encouraging. Unlike the advisor briefing, this template avoids technical machine-learning terminology and emphasizes actionable next steps without presenting a prediction as a certain outcome.

**Prompt Structure:** The template receives the same input fields as Template 1 but requests a warm tone, accessible language, and approximately two to three realistic support suggestions.

**Illustrative Example Input:**
- Predicted status: Dropout
- Dropout probability: 0.76
- Important factors: Low academic progress and tuition status not up to date
- Cluster profile: Students with academic and financial support needs

**Illustrative Example Output:**

"We would like to check in and see how your studies are going. Your academic advisor can help you review your progress and explore study strategies that may be useful. You can also contact student services to check your tuition status and learn about available support options. If you would like assistance planning your next steps, consider arranging a meeting with your advisor."

**Assumptions and Limitations:**
- Messages must not reveal sensitive predictions unnecessarily.
- The system should not label students as guaranteed dropouts.
- Generated messages must be reviewed before being sent.
- The model must not invent personal circumstances, financial balances, attendance, or academic records.

## 4. Comparison of Prompt Designs

| Criterion | Advisor Briefing | Student Outreach |
|---|---|---|
| Audience | Academic advisors | Students |
| Tone | Professional and analytical | Warm and supportive |
| Focus | Risk interpretation and interventions | Encouragement and next steps |
| Technical detail | Moderate | Minimal |
| Intended length | 120–160 words | 90–130 words |
| Human review | Required | Required before sending |

These templates serve different communication purposes. Their evaluation should therefore consider suitability for the intended audience, not only which template receives a higher overall score.

## 5. Implementation and Safety

Both templates are implemented in `Generative_AI/genai_utils.py` using the shared function:

`generate_briefing(student, prediction, probs, top_features, cluster_profile, template)`

The system uses the Gemini API and reads its key from the `GEMINI_API_KEY` environment variable. The key must never be committed to GitHub.

The prompts instruct the model to use only supplied student information, avoid fabricated claims, and present predictions as uncertain.

Global feature importance must not be treated as an individual explanation or evidence of causation. For example, a tuition status that is not up to date does not prove a specific outstanding balance, and zero recorded evaluations does not prove student absence.

The dashboard uses information available at the early prediction stage and excludes second-semester features and the actual target label from the student information sent to Gemini.

Cluster information is used only when a valid cluster profile is available. If the profile is unavailable, the model must not invent cluster membership or characteristics.

Generated recommendations support academic decision-making but do not replace professional judgment. Human review is required before acting on a briefing or sending an outreach message.

## 6. Next Steps

The two templates will be tested with multiple student scenarios, including at least three cases per template.

Their outputs will be assessed for relevance, clarity, completeness, personalization, factual accuracy, and readability. Quantitative measures may include response length, keyword alignment, readability scores, and simulated user preference.

Testing results, comparative analysis, and final template selection will be documented separately as part of the team's Generative AI evaluation work.
