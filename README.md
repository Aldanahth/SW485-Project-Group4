
# University Student Retention & Advisory Dashboard

**Course:** SWE485  
**Group:** 4

## Project Overview

This project focuses on analyzing university student data to identify factors associated with academic performance, student retention, and dropout.

The project aims to explore patterns in student characteristics and academic outcomes and establish a foundation for developing a student retention and advisory dashboard that can support early identification of students at risk of dropping out.

## Motivation

Student dropout is an important challenge for universities because it affects students' academic progress and institutional retention rates. We chose this problem to explore how student characteristics and academic performance can help identify students who may need additional support.

The selected UCI dataset provides relevant demographic, financial, and academic information for investigating these patterns and supporting the development of an early-warning advisory dashboard.

## Dataset Description

The dataset contains **4,424 student records and 37 columns**, consisting of **36 input features** and one target variable.

The features include demographic, socioeconomic, financial, and academic information. The target variable, `Target`, represents three student outcomes: **Graduate, Dropout, and Enrolled**.

The dataset was obtained from the UCI Machine Learning Repository:

[Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

The original dataset is available in `Dataset/data.csv`, and its source and licensing information are documented in `Dataset/dataset_info.txt`.

## Phase 1: Data Exploration

The data exploration and preprocessing steps are documented in `Phase1_Data_Exploration.ipynb`.

The notebook covers:

- Dataset selection and justification.
- Initial inspection of dataset dimensions, structure, and data types.
- Assessment and visualization of missing values.
- Descriptive statistical analysis.
- Analysis and visualization of the target class distribution.
- Exploratory data analysis using histograms, box plots, and correlation analysis.
- Mutual information analysis to identify features associated with student outcomes.
- Comparisons of academic, financial, demographic, and course-related attributes across target classes.
- Preprocessing pipeline and the preprocessed dataset.
- Key insights and challenges identified during exploration.
- Consideration of prediction timing to support early identification of at-risk students.

### Initial Data Inspection

The dataset contains 4,424 records, with no missing values identified during the initial inspection.

The target classes are unevenly distributed:

| Target Class | Number of Records | Percentage |
| ------------ | ----------------: | ---------: |
| Graduate     |             2,209 |      49.9% |
| Dropout      |             1,421 |      32.1% |
| Enrolled     |               794 |      17.9% |

Because of this class imbalance, model evaluation should consider per-class precision, recall, and F1-score in addition to accuracy.

### Key Insights

Exploratory analysis identified several important patterns:

- **Academic performance:** First- and second-semester academic features show strong associations with student outcomes.
- **Financial factors:** Tuition payment status, scholarship status, and debtor status are associated with differences in dropout rates.
- **Student characteristics:** Age at enrollment, gender, and course show differences across student outcomes.
- **Feature relationships:** Several first- and second-semester academic variables are strongly correlated.
- **Data quality:** No missing values were identified, but categorical variables encoded as integers and zero semester grades require careful interpretation.

These findings describe associations observed during exploration and do not establish cause-and-effect relationships.

### Prediction Timing and Preprocessing

The team selected **prediction after the first semester** as the intended early-warning point.

This approach allows the model to use enrollment-time information and first-semester academic performance while excluding all six second-semester features to avoid using information from the future.

The preprocessing pipeline includes:

- Removing the six second-semester features.
- Splitting the dataset into training and testing sets using an **80/20 stratified split**.
- Encoding categorical features.
- Scaling numerical features using parameters fitted on the training data only to prevent data leakage.

The resulting preprocessed dataset is saved in `Dataset/preprocessed_data.csv`. It contains **102 processed features**, the `Target` column, and a column identifying the train/test split.

## Phase 1: Supervised Learning

The supervised learning work is documented in `Phase1_Supervised_Learning.ipynb`.

Two models were trained and tuned on the shared preprocessed dataset using the same train/test split, `random_state=42`, 5-fold stratified cross-validation, macro F1 as the tuning metric, and `class_weight="balanced"`:

- **Model 1: Random Forest**, with hyperparameter tuning and feature-importance analysis.
- **Model 2: Logistic Regression**, with tuning of the regularization strength `C`.

Both models were evaluated using the same evaluation approach, including accuracy, per-class precision, recall, F1-score, confusion matrices, 5-fold cross-validation, and McNemar's test on the test-set predictions.

### Results Summary

| Model | Test Accuracy | Test Macro F1 | 5-Fold CV Macro F1 |
| ----- | ------------: | ------------: | -----------------: |
| Random Forest | 74.1% | 0.673 | 0.694 |
| Logistic Regression | 71.1% | 0.672 | 0.684 |

- **Recommended model for Phase 2: Random Forest.** It achieved higher test accuracy and a marginally higher test macro F1 than Logistic Regression, as well as a higher cross-validation macro F1. The test accuracy difference was statistically significant according to McNemar's test (`p = 0.026`). Random Forest also provides class probabilities and feature importances for the dashboard. Logistic Regression is retained as an interpretable baseline.
- **Main challenge:** The **Enrolled** class is difficult to predict for both models. Random Forest achieved an Enrolled F1-score of approximately 0.43, while Logistic Regression achieved approximately 0.47. Random Forest had higher Enrolled precision (0.46 versus 0.39), while Logistic Regression had higher Enrolled recall (0.59 versus 0.42). Students who are still enrolled can have academic patterns similar to both future graduates and future dropouts after one semester.
- **Evaluation artifacts:** Evaluation tables, confusion-matrix heatmaps, and plots are saved in `Supervised_Learning/evaluation_results/` and `Supervised_Learning/plots/`.

*The results above match the final reported evaluation outputs and Section 3.8 of Notebook 2. If the notebook is re-run, the results and written explanations should be checked again.*

### Reproducibility and Dependencies

The repository includes `requirements.txt`, documenting the Python library versions used in the final Google Colab run of Notebook 2. These versions were recorded from the same session that produced the reported evaluation results.

The main dependencies are:

- `pandas==2.2.3`
- `numpy==2.1.3`
- `scikit-learn==1.6.1`
- `scipy==1.16.3`
- `matplotlib==3.10.0`
- `seaborn==0.13.2`
- `joblib==1.6.0`

To install the documented dependencies, run:

`pip install -r requirements.txt`

Different library versions, especially scikit-learn, may lead to different tuned hyperparameters and evaluation results.

## Repository Structure

```text
SW485-Project-Group4/
├── Dataset/
│   ├── data.csv
│   ├── preprocessed_data.csv
│   └── dataset_info.txt
├── Supervised_Learning/
│   ├── models/               # saved tuned models
│   ├── evaluation_results/   # metrics tables, confusion matrices, predictions
│   └── plots/                # saved visualizations
├── docs/
│   ├── task_distribution.md      # roles, responsibilities, deadlines, milestones
│   ├── individual_reflections.md # each member's reflection
│   └── peer_review.md            # peer reviews between team members
├── Phase1_Data_Exploration.ipynb
├── Phase1_Supervised_Learning.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Group Members

| Student Name | Student ID |
| ------------ | ---------- |
| الدانة ال ثنيان | 445201311 |
| نجد الغانم | 445200363 |
| ساره الجبرين | 445201223 |
| يسرى ال هلال | 445200254 |
| جمانة العنزي | 445200400 |
| اريام الركيان | 445200057 |

## Team Work and Documentation

- Task distribution, shared responsibilities, and milestones: [`docs/task_distribution.md`](docs/task_distribution.md)
- Individual reflections: [`docs/individual_reflections.md`](docs/individual_reflections.md)
- Peer reviews: [`docs/peer_review.md`](docs/peer_review.md)



## AI Tools Disclosure

AI tools were used as supporting resources during the project. All AI-assisted content was reviewed and verified by the relevant team members, who remain responsible for the accuracy of their work and the final project deliverables.

**ChatGPT (OpenAI) — Aldanah Al Thenyan:** Used to assist with documentation drafting, language refinement, reviewing exploratory data analysis findings, and providing code suggestions and debugging assistance for the missing-values visualization. Aldanah independently reviewed the AI-assisted content, checked its consistency with the project's notebooks and evaluation results, and verified the accuracy of the documentation before submission.

**Claude (Anthropic) — Sarah Aljabrain:** Used to assist with selected parts of the project, including writing, code structuring, and interpretation of evaluation results. Sarah reviewed and edited the AI-assisted outputs and remains responsible for their accuracy.

**Claude (Anthropic) — Yusra Alhilal:** Used as a supporting reference for code clarification and refining the phrasing and formatting of documentation. Yusra retains full responsibility for the technical implementation, analysis, and accuracy.

AI tools supported the team's work but did not replace independent analysis, review, or verification by the team members.

