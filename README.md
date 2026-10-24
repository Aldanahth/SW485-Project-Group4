
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

The supervised learning work is in `Phase1_Supervised_Learning.ipynb`. Two models were trained and tuned on the shared preprocessed dataset (same train/test split, `random_state=42`, 5-fold stratified cross-validation, macro F1 as the tuning metric, `class_weight="balanced"`):

- **Model 1: Random Forest**, with hyperparameter tuning and a feature-importance analysis.
- **Model 2: Logistic Regression**, with tuning of the regularization strength `C`.

Both models were then evaluated with the same evaluation function (accuracy, per-class precision/recall/F1, confusion matrices, 5-fold cross-validation, and a McNemar test on the test-set predictions).

### Results summary

| Model               | Test accuracy | Test macro F1 | 5-fold CV macro F1 |
| ------------------- | ------------: | ------------: | -----------------: |
| Random Forest       |         74.1% |         0.673 |              0.694 |
| Logistic Regression |         71.1% |         0.672 |              0.684 |

- **Recommended model for Phase 2: Random Forest.** It achieved higher test accuracy and a marginally higher test macro F1 than Logistic Regression, as well as a higher cross-validation macro F1. The test accuracy difference is statistically significant (McNemar p = 0.026). Random Forest also provides class probabilities and feature importances for the dashboard. Logistic Regression is retained as an interpretable baseline.
- **Main challenge:** the *Enrolled* class is difficult to predict for both models. Random Forest achieved an Enrolled F1-score of approximately 0.43, while Logistic Regression achieved approximately 0.47. Students who are still enrolled can have academic patterns similar to both future graduates and future dropouts after one semester.
- Evaluation tables, confusion-matrix heatmaps, and plots are also saved in `Supervised_Learning/evaluation_results/` and `Supervised_Learning/plots/`.

*The results above match the saved evaluation outputs and Section 3.8 of the committed notebook. If the notebook is re-run, the results and written explanations should be checked again.*

The repository includes `requirements.txt` for documenting the project's Python dependencies. However, the versions currently listed in this file do not fully match the versions printed in the saved Notebook 2 run. The file should be regenerated from the same environment used for the final accepted results before submission. Different library versions, especially scikit-learn, may produce different tuned hyperparameters and evaluation results.

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

| Student Name    | Student ID |
| --------------- | ---------- |
| الدانة ال ثنيان | 445201311  |
| نجد الغانم      | 445200363  |
| ساره الجبرين    | 445201223  |
| يسرى ال هلال    | 445200254  |
| جمانة العنزي    | 445200400  |
| اريام الركيان   | 445200057  |

## Team Work and Documentation

- Task distribution, shared responsibilities, and milestones: [`docs/task_distribution.md`](docs/task_distribution.md)
- Individual reflections: [`docs/individual_reflections.md`](docs/individual_reflections.md)
- Peer reviews: [`docs/peer_review.md`](docs/peer_review.md)

## AI Tools Disclosure

ChatGPT was used to assist with documentation drafting, language refinement, reviewing exploratory data analysis findings, and providing code suggestions and debugging assistance for the missing-values visualization.

The team reviewed the AI-assisted content and is responsible for verifying the accuracy of the analysis, code, and final project deliverables.

Any additional AI-assisted work will be disclosed as appropriate.

Claude (Anthropic) was used to assist with selected parts of the project, including writing, code structuring, and interpretation of evaluation results. All outputs were reviewed and edited by ساره الجبرين, who is responsible for their accuracy.

Claude (Anthropic) was used purely as a supporting reference for code clarification and for refining the phrasing and formatting of the documentation. Yusra holds full ownership of the technical implementation, analysis, and accuracy.
