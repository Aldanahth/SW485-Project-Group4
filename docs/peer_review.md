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