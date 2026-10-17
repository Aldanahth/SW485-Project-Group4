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
|---|---:|---:|
| Graduate | 2,209 | 49.9% |
| Dropout | 1,421 | 32.1% |
| Enrolled | 794 | 17.9% |

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

The supervised learning work is assigned to `Phase1_Supervised_Learning.ipynb`.

This notebook is intended to cover:

- Random Forest model training and hyperparameter tuning.
- Training and tuning a second classification model using SVM or Logistic Regression.
- Feature importance analysis where applicable.
- Model evaluation using accuracy, precision, recall, and F1-score.
- Confusion matrices and 5-fold cross-validation.
- Comparison of model performance and analysis of misclassifications.
- Selection of a recommended model for Phase 2.

## Repository Structure

```text
SW485-Project-Group4/
├── Dataset/
│   ├── data.csv
│   ├── preprocessed_data.csv
│   └── dataset_info.txt
├── Phase1_Data_Exploration.ipynb
├── Phase1_Supervised_Learning.ipynb
├── .gitignore
└── README.md
```

## Group Members

| Student Name | Student ID |
|---|---|
| الدانة ال ثنيان | 445201311 |
| نجد الغانم | 445200363 |
| ساره الجبرين | 445201223 |
| يسرى ال هلال | 445200254 |
| جمانة العنزي | 445200400 |
| اريام الركيان | 445200057 |

## Team Contributions

The responsibilities for Phase 1 were distributed among the six team members. Each member is responsible for implementing her assigned tasks, documenting the results, and contributing her work to the GitHub repository.

| Student Name | Role | Phase 1 Responsibilities | Deadline |
|---|---|---|---|
| الدانة ال ثنيان | Data Inspection & Repository Management | Load and inspect the dataset; examine dimensions, data types, missing values, descriptive statistics, and target class distribution; set up and maintain the GitHub repository and README; collaborate on Key Insights & Challenges. | October 20, 2026 |
| يسرى ال هلال | Exploratory Data Analysis | Create histograms, box plots, correlation heatmaps, and feature-versus-target visualizations; document the dataset source and justification; collaborate on Key Insights & Challenges. | October 20, 2026 |
| نجد الغانم | Data Preprocessing | Encode categorical features, scale numerical features, prepare a stratified train/test split, address class imbalance as appropriate, export `preprocessed_data.csv`, and document preprocessing decisions. | October 15, 2026 |
| اريام الركيان | Random Forest Model | Explain the model selection, train a Random Forest classifier, tune hyperparameters, and analyze feature importance. | October 19, 2026 |
| جمانة العنزي | Second Classification Model | Select and justify SVM or Logistic Regression, train the classifier, and tune hyperparameters. | October 19, 2026 |
| ساره الجبرين | Model Evaluation & Comparison | Evaluate both models using accuracy, precision, recall, F1-score, confusion matrices, and 5-fold cross-validation; compare model performance; recommend a model for Phase 2; write the Introduction & Problem Statement and task distribution document. | October 20, 2026 |

### Shared Responsibilities

- Each member writes and executes the code for her assigned section and explains the results.
- الدانة ال ثنيان and يسرى ال هلال collaborate on the Key Insights & Challenges section.
- Each member reviews another member's work according to the agreed peer-review rotation.
- Each member provides a short individual reflection describing what she learned and the challenges she encountered.
- Both notebooks must be executed from the beginning and reviewed before final submission.

### Individual Reflections

Individual reflections will be added after each team member provides a short account of her learning experience, contributions, and challenges during Phase 1.

### Phase 1 Milestones

| Date | Milestone |
|---|---|
| October 15, 2026 | Complete and share the preprocessed dataset. |
| October 19, 2026 | Complete model training and hyperparameter tuning. |
| October 20, 2026 | Complete model evaluation, comparison, and README documentation. |
| October 21, 2026 | Restart and run both notebooks, verify outputs, and review the repository. |
| October 22, 2026 | Final Phase 1 submission. |

## AI Tools Disclosure

ChatGPT was used to assist with documentation drafting, language refinement, reviewing exploratory data analysis findings, and providing code suggestions and debugging assistance for the missing-values visualization.

The team reviewed the AI-assisted content and is responsible for verifying the accuracy of the analysis, code, and final project deliverables.

Any additional AI-assisted work will be disclosed as appropriate.
