# Prompt Design Rationale

## 1. Overview

The University Student Retention & Advisory Dashboard uses Google Gemini 2.5 Flash to generate supportive academic guidance based on supervised learning predictions, relevant student features, and clustering profiles.

Two prompt templates were designed for different users: academic advisors and students. Both templates use the same structured input data but differ in their intended audience, tone, level of detail, and recommended actions.

## 2. Template 1: Advisor Briefing

**Template ID:** `advisor`

**Intended Use Case:** Generate a professional academic briefing to help university advisors understand a student's predicted academic status and identify suitable support interventions.

**Design Rationale:** Academic advisors need concise, evidence-based information to prioritize support. This template uses a structured, professional style and requests a summary of predicted status, important factors, cluster characteristics, and two to three practical interventions.

**Prompt Structure:** The template receives `{student}`, `{prediction}`, `{probs}`, `{top_features}`, and `{cluster_profile}`. It instructs Gemini to use only the provided evidence, distinguish predictions from facts, and avoid unsupported assumptions.

**Illustrative Example Input:**
- Predicted status: Dropout
- Dropout probability: 0.76
- Important factors: Low academic progress and outstanding tuition fees
- Cluster profile: Students with academic and financial support needs

**Illustrative Example Output:**

"The student is predicted to be at elevated risk of dropping out. Relevant factors include academic progress and tuition status. An academic advisor should review the student's recent academic performance, discuss available financial support resources, and arrange a follow-up meeting. This prediction is a decision-support indicator, not a confirmed outcome."

**Assumptions and Limitations:**
- Model predictions may be incorrect.
- Feature importance does not establish causation.
- Cluster descriptions are generalized patterns, not individual diagnoses.
- Recommendations require human review before action.

## 3. Template 2: Student Outreach

**Template ID:** `student`

**Intended Use Case:** Generate a supportive outreach message that encourages a student to seek academic assistance.

**Design Rationale:** Student-facing communication should be understandable, respectful, and encouraging. Unlike the advisor briefing, this template avoids technical machine-learning terminology and emphasizes actionable next steps without presenting a prediction as a certain outcome.

**Prompt Structure:** The template receives the same input fields as Template 1 but requests a warm tone, accessible language, and approximately two to three realistic support suggestions.

**Illustrative Example Input:**
- Predicted status: Dropout
- Dropout probability: 0.76
- Important factors: Low academic progress and outstanding tuition fees
- Cluster profile: Students with academic and financial support needs

**Illustrative Example Output:**

"We would like to check in and see how your studies are going. If you are facing academic or financial challenges, support may be available. Consider arranging a meeting with your academic advisor to discuss study strategies and available university resources. Your current circumstances do not determine your future success, and there are steps you can take to move forward."

**Assumptions and Limitations:**
- Messages must not reveal sensitive predictions unnecessarily.
- The system should not label students as guaranteed dropouts.
- The generated message must be reviewed before being sent.
- The model must not invent personal circumstances or academic records.

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

The prompts instruct the model to use only supplied student information, avoid fabricated claims, and present predictions as uncertain. Generated recommendations support academic decision-making but do not replace professional judgment.

## 6. Next Steps

The two templates will be tested with multiple student scenarios. Their outputs will be assessed for relevance, clarity, completeness, personalization, factual accuracy, and readability. Testing results and final template selection will be documented separately.
