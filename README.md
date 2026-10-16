# University Student Retention & Advisory Dashboard

**Course:** SWE485  
**Group:** 4

## Project Overview

This project focuses on analyzing university student data to identify factors associated with academic performance, student retention, and dropout.

The project aims to explore patterns in student characteristics and academic outcomes and establish a foundation for developing a student retention and advisory dashboard that can support early identification of students at risk of dropping out.

## Dataset Description

The dataset contains **4,424 student records and 37 columns**, consisting of **36 input features** and one target variable.

The features include demographic, socioeconomic, financial, and academic information. The target variable, `Target`, represents three student outcomes: **Graduate, Dropout, and Enrolled**.

The dataset was obtained from the UCI Machine Learning Repository:

[Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

The dataset is available in `Dataset/data.csv`, and its source and licensing information are documented in `dataset_info.txt`.

## Phase 1: Data Exploration

The initial data exploration is documented in `Phase1_Data_Exploration.ipynb`.

The notebook covers:

- Dataset selection and justification.
- Initial inspection of dataset dimensions, structure, and data types.
- Assessment of missing values.
- Descriptive statistical analysis.
- Analysis and visualization of the target class distribution.
- Exploratory data analysis using histograms, box plots, and correlation analysis.
- Mutual information analysis to identify features associated with student outcomes.
- Comparisons of academic, financial, demographic, and course-related attributes across target classes.
- Preprocessing pipeline and the preprocessed dataset.
- Key insights and challenges identified during exploration.
- Consideration of prediction timing to support early identification of at-risk students.

### Initial Data Inspection

The dataset contains 4,424 records with no missing values identified during the initial inspection.

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

### Prediction Timing

The team selected **prediction after the first semester** as the intended early-warning point.

This approach allows the model to use enrollment-time information and first-semester academic performance while excluding all six second-semester features to avoid using information from the future.

The 6 second-semester features were removed, the data was split 80/20 (stratified), and categories were encoded and numeric features scaled using the training data only. The result is saved as Dataset/preprocessed_data.csv (102 features, Target, and a split column).

## Repository Structure

```text
SW485-Project-Group4/
├── Dataset/
│   ├── data.csv
│   ├── preprocessed_data.csv
│   └── dataset_info.txt
├── Phase1_Data_Exploration.ipynb
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

## AI Tools Disclosure

