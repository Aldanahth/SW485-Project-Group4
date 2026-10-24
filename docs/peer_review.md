

# Peer Review: Initial Data Inspection and Repository

**Reviewer:** ساره الجبرين (Member 6, Evaluation & comparison)  
**Reviewed member:** الدانة ال ثنيان (Member 1, Data inspection & repository)  
**Reviewed material:** *Initial Data Inspection* section of `Phase1_Data_Exploration.ipynb`, and the repository README

## What was checked

- I re-ran the key numbers from the raw file `Dataset/data.csv` and compared them with the notebook text.
- I read each code cell, its output, and the explanation written below it.

## What works well

- **The numbers in the explanations are correct.** I recomputed them from the raw data: 4,424 rows and 37 columns; 29 integer, 7 float and 1 text column; average age at enrollment 23.27; average admission grade 126.98; average first-semester grade 10.64 and second-semester grade 10.23; class counts Graduate 2,209, Dropout 1,421, Enrolled 794.
- **Every output is followed by a short interpretation**, including useful warnings (for example, that some numeric columns are really category codes and should not be read as measurements).
- **The class-imbalance observation is linked to later work** (evaluation with per-class metrics), which is exactly what the models section needed.
- **Dataset loading is robust:** it checks the common paths and falls back to an upload prompt.
- **The README is clear:** it gives the project motivation, dataset description, class-distribution table, member names and IDs, and the repository structure.

## Suggestions for improvement

1. **Missing-values chart.** It prints "Glyph 9 missing from font" and "Tight layout not applied" warnings. The cause is the column name `Daytime/evening attendance` followed by a hidden tab character in the raw file. Stripping the column names right after loading (`df.columns = df.columns.str.strip()`) would fix the warnings and the cramped x-axis labels. Since the dataset has no missing values, the chart is a flat line of zeros; a one-line statement may be enough, or the chart could be kept with a short note that its purpose is to confirm completeness.
2. **Add a preview of the data** (`df.head()`) near the beginning of the inspection, so readers can see what a row looks like before reading the data types and statistics.
3. **Introduction & Problem Statement.** The handbook lists this as the first section of the notebook, and it was missing. It has now been added at the top of the notebook.
4. **README milestones.** The milestones table listed October 22 as the final submission; it has been updated to October 24 after the extension.
5. **Library versions.** Adding a `requirements.txt` would make the notebooks reproducible on every machine. This matters because the tuned `C` of the Logistic Regression model can switch between two nearly tied values depending on the environment.

## Overall

The inspection section is accurate, clear, and well explained. The suggestions above are small polish items; none of them changes the results.


---

# Peer Review: Exploratory Data Analysis

**Reviewer:** الدانة ال ثنيان (Member 1, Data inspection & repository)  
**Reviewed member:** يسرى ال هلال (Member 2, Exploratory data analysis)  
**Reviewed material:** *Exploratory Data Analysis* section of `Phase1_Data_Exploration.ipynb`

## What was checked

- I read the histograms, box plots, correlation heatmap, mutual information analysis, binary-feature charts, and the dropout-by-course chart, together with the written observations under each one.

## What works well

- **Categorical codes are separated from continuous features.** Columns such as `Course` and `Marital status` are not treated as numbers, which avoids misleading histograms and correlations.
- **Mutual information is used instead of correlation with the target**, which is the correct choice when the target is made of classes.
- **The observations use real numbers and careful wording.** For example, dropout is about 87% for students whose tuition fees are not up to date versus about 25% for those who pay on time, and the text says "associated with" and not "causes".
- **Limits are stated honestly.** The comparison for international students is marked as less reliable because only 110 students are international.
- **The prediction-timing note links the analysis to the team decision** to predict after the first semester.

## Suggestions for improvement

1. **Update the heatmap observation.** It says the team "can consider" combining the correlated semester features, but this was already done in preprocessing (the six 2nd-semester features were removed and `academic_progress` was added). The text can say that the redundancy was addressed.
2. **Add the colour scale meaning** to the heatmap observation (for example, which correlations are considered strong), so readers can interpret the figure without guessing.

## Overall

The exploratory analysis is accurate, careful, and clearly connected to the later steps. The suggestions are small wording updates.

---

# Peer Review: Preprocessing Pipeline

**Reviewer:** يسرى ال هلال (Member 2, Exploratory data analysis)  
**Reviewed member:** نجد الغانم (Member 3, Data preprocessing)  
**Reviewed material:** *Preprocessing Pipeline* and *Preprocessed Dataset Ready for Modeling* sections of `Phase1_Data_Exploration.ipynb`, and `Dataset/preprocessed_data.csv`

## What was checked

- I re-ran the preprocessing cells and reloaded the saved file.
- I checked that each step matches the team decision (prediction after the 1st semester) and the findings of the exploratory analysis.

## What works well

- **The steps are in the correct order to prevent data leakage:** the train/test split is done before rare-category grouping, one-hot encoding, and scaling, and all three are learned from the training data only.
- **The split is reproducible and fair:** 80/20, stratified, `random_state=42`, with the same class percentages in the full data, the training set, and the test set.
- **The six 2nd-semester features were removed**, as agreed by the team.
- **The zero-enrolled case is handled carefully:** `academic_progress` avoids division by zero, and the `no_units_enrolled` flag keeps the 180 affected students separate.
- **Categorical codes are treated as categories**, which matches the exploratory finding that columns such as `Course` are labels, not quantities.
- **The saved file was verified:** 4,424 rows, 104 columns, and no missing values.

## Suggestions for improvement

1. **Step 7 numbers:** the text says father's occupation has 46 values, while the printed output shows 41. Both are correct (46 in the full dataset, 41 in the training set), so the text should state both to avoid confusion.
2. **Save the fitted preprocessing objects** (rare-category rules, one-hot encoder, and scaler) so that Phase 2 can transform raw student inputs into the 102 model columns.
3. **Phase 2 pipeline:** the grouping, encoder, and scaler were fitted on the whole training set before cross-validation, so each validation fold had a very small influence on them. A scikit-learn `Pipeline` in Phase 2 would remove this.

## Overall

The preprocessing is correct, leakage-free, and well documented, and it follows the team decision.

---

# Peer Review: Random Forest Model

**Reviewer:** نجد الغانم (Member 3, Data preprocessing)  
**Reviewed member:** اريام الركيان (Member 4, Random Forest model)  
**Reviewed material:** *Model 1: Random Forest Classifier* in `Phase1_Supervised_Learning.ipynb`

## What was checked

- I read the model selection rationale and ran the code cells to compare the printed results with the preprocessed data.

## What works well

- **The rationale is clear:** it explains why Random Forest fits a multi-class problem with mixed features, and lists strengths and weaknesses.
- **The setup is fair:** it uses the shared train/test split from `preprocessed_data.csv`, 5-fold stratified cross-validation, `random_state=42`, and `class_weight="balanced"`, the same as the second model.
- **Tuning is done properly:** `GridSearchCV` tests 27 combinations of `n_estimators`, `max_depth`, and `min_samples_split` with macro F1 as the metric, and the baseline (macro F1 0.663) is compared with the tuned model (0.678).
- **The evaluation is complete:** a classification report per class, a confusion matrix, and the top-10 feature importances (the top ones are `academic_progress`, first-semester approved units, and first-semester grade).
- **The limitation of feature importance is stated:** the scores do not establish causation.

## Suggestions for improvement

1. **Add a written interpretation** after the results, explaining the weak *Enrolled* class and the top features, so the reader does not need to read the output alone.
2. **Fix one rationale sentence:** it says Random Forest is less sensitive to missing values, but the dataset has no missing values, so the sentence does not apply here.
3. **Mention library versions:** the selected settings can change with the scikit-learn version, so a note pointing to `requirements.txt` would help reproducibility.

## Overall

The Random Forest model is trained, tuned, and evaluated correctly and fairly. The suggestions are about explanation and reproducibility, not about the results.

---

# Peer Review: Logistic Regression Model

**Reviewer:** اريام الركيان (Member 4, Random Forest model)  
**Reviewed member:** جمانة العنزي (Member 5, Second classification model)  
**Reviewed material:** *Model 2: Logistic Regression* in `Phase1_Supervised_Learning.ipynb`

## What was checked

- I read the model selection rationale and ran the code cells to compare the printed results with the preprocessed data.

## What works well

- **The choice of model is justified:** the rationale lists strengths (interpretability, efficiency, a baseline for comparison) and weaknesses (linear boundaries, sensitivity to preprocessing, class imbalance).
- **The setup matches Model 1:** the same split, 5-fold stratified cross-validation, `random_state=42`, and `class_weight="balanced"`, which makes the comparison fair.
- **Tuning is clear:** five values of `C` are tested, and the tuning table shows the mean macro F1, standard deviation, and rank. `max_iter=3000` avoids convergence warnings.
- **The evaluation is complete:** test accuracy, macro F1, a per-class report, and a confusion matrix.

## Suggestions for improvement

1. **Explain the near tie:** `C = 1` (0.6846) and `C = 0.1` (0.6845) are almost equal, so the selected value can change between machines. A sentence saying this would prevent confusion if someone re-runs the notebook.
2. **Add a written interpretation** after the results, especially for the weak *Enrolled* class.
3. **Show the coefficients:** interpretability is the main strength of this model, so a short look at the largest coefficients would support the rationale.

## Overall

The Logistic Regression model is trained, tuned, and evaluated correctly and consistently with Model 1. The suggestions are about explanation, not about the results.

---

# Peer Review: Model Evaluation & Comparison

**Reviewer:** جمانة العنزي (Member 5, Second classification model)  
**Reviewed member:** ساره الجبرين (Member 6, Evaluation & comparison)  
**Reviewed material:** *Model Evaluation & Comparison* sections of `Phase1_Supervised_Learning.ipynb`, and the files in `Supervised_Learning/evaluation_results/`

## What was checked

- I ran the evaluation cells and compared the printed numbers with the saved CSV files and the results table in the README.

## What works well

- **One shared evaluation function** is used for both models, so the metrics are computed in exactly the same way.
- **The metrics fit the class imbalance:** macro F1 is the main metric, with per-class precision, recall, and F1, confusion matrices (counts and row percentages), and 5-fold cross-validation.
- **The comparison is careful:** it includes a McNemar test (p = 0.026), a list of the most frequent mistakes, and how often the two models are right or wrong on the same students.
- **The conclusion matches the numbers:** Random Forest is recommended (72.5% accuracy, macro F1 0.678) and the weak *Enrolled* class is explained.
- **Next Steps for Phase 2** are specific and connected to the results.

## Suggestions for improvement

1. **Results depend on the environment:** the selected hyperparameters can change with the scikit-learn version, so `requirements.txt` should be kept in the repository and mentioned next to the results.
2. **The weak class is described but not improved:** threshold tuning for *Enrolled* is proposed for Phase 2, and a first experiment would strengthen the recommendation.
3. **The coefficient plot** shows only the Dropout class, so adding the other classes would give the full picture of the model.

## Overall

The evaluation is complete, fair, and consistent with the numbers in the README. The suggestions are about reproducibility and possible Phase 2 improvements.