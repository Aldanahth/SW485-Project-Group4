# Individual Reflections

Each team member reflects below on what she learned and the challenges she faced during Phase 1.

---

## الدانة ال ثنيان
*Data Inspection & Repository Management*

### What I Learned

I learned that understanding the dataset is an important first step before starting any analysis. I used Python to check the number of rows and columns, the data types, and basic statistics, which gave me a clear idea of what the dataset contains and how it is organized.

I also learned how to check for missing values and visualize them. Even though our dataset had no missing values, I understood why this step is necessary before working with the data, and creating the chart helped me practice presenting information in a way that is easy to understand.

Analyzing the target class distribution showed me that Graduate is the largest class and Enrolled is the smallest. This made me realize that the classes are imbalanced and that we should keep this in mind when evaluating our models.

Working with GitHub also developed my existing skills. Although I had used it before, this project gave me more experience in organizing a repository, managing project files, and updating the README for the team. I also became more comfortable using Google Colab, running code cells in the correct order, and saving notebooks with their results.

Overall, this project improved my Python skills and helped me understand the importance of data inspection, clear documentation, and teamwork. I feel more confident working with datasets and managing my contribution to a group project.

---

## يسرى ال هلال
*Exploratory Data Analysis*

### What I Learned

Before this project, I thought that if a column contained numbers, I could simply treat it as a number. I learned that some columns, such as Course, use numbers only as labels, so I now check what each column really means before working with it.

I also learned that not every method works in every case. At first, I used correlation with the target, but a teammate explained that it does not work well when the target is made of categories. That is when I learned about mutual information and why it was a better choice here.

Working on the charts taught me how to read them and not only how to make them. I learned to ask what each chart is really showing and to describe it in simple words, using real numbers from the data. I also learned to be careful with my wording: two things appearing together does not mean that one causes the other, so I use "associated with" instead of saying that something causes dropout.

The prediction-timing issue made me think about how the system would work in real life. A model can look very good, but if it uses information we do not have yet, it is not useful.

Finally, I learned how helpful teamwork can be. My teammates found mistakes that I had not noticed, and fixing them made our work much better.

---

## نجد الغانم
*Data Preprocessing*

### What I Learned

I learned how to decide which data a model should use, and that every choice is a trade-off. Our system is meant to help academic advisors warn students early. The dataset records six results for each of the two semesters: credited, enrolled, evaluated, and approved units, the grade, and units without evaluation. The second-semester results would make the model more accurate, but they only exist after the second semester ends, which is too late for an early warning. As a team, we compared the options, decided not to use the second-semester data, and chose to warn the advisor at the end of the first semester. I then cleaned the data to match that decision.

I also learned how to adapt when the data does not match the plan. The suggested dashboard includes GPA and attendance sliders, but when I checked the column names, I found that the dataset has no attendance column. I proposed to my teammates that we use what the data already has, and we agreed on an academic progress measure: approved units divided by enrolled units. While preparing it, an AI tool inspected the data and found a special case: 180 students enrolled in zero units, which makes the division impossible, and it helped us flag them. It also gave me a brief on the order of the steps, which showed me that cleaning data is a series of decisions. As a beginner, I ran every step myself and checked each output.

Finally, I learned that a number does not always mean a quantity. Codes such as Course are labels, not measurements, so they need different handling from real numbers.

---

## اريام الركيان
*Random Forest Model*

> **Preliminary draft: Aryam should review, edit, and confirm that it reflects her own experience before submission.**

### What I Learned

I learned that Random Forest suits our problem well: the dataset mixes numerical and categorical features, the task has three classes (Dropout, Enrolled, Graduate), and the model handles non-linear relationships without needing extensive feature scaling. It combines many decision trees, which makes it more robust against overfitting than a single tree.

I also learned how much hyperparameter tuning matters. I used GridSearchCV with 5-fold stratified cross-validation to compare 27 combinations of settings and selected the best one using macro F1. The best settings were 100 trees, a maximum depth of 20, and a minimum of 10 samples to split a node. This showed me that model performance depends on its settings and that they should be chosen with cross-validation, not guessed.

Analyzing feature importance taught me that the scores show which features the model relies on most, but they do not prove that those features cause dropout. I also learned about the limits of the model: it is harder to interpret than simpler models, tuning many combinations takes more computation, and it can still overfit if its depth is not controlled.

---

## جمانة العنزي
*Second Classification Model*

### What I Learned

Before this project, I thought that building a machine learning model was mostly about choosing an algorithm, training it, and checking its accuracy. I learned that there is much more to it, especially when predicting student outcomes across three classes: Dropout, Enrolled, and Graduate.

I learned that different models approach prediction differently. Logistic Regression works differently from Random Forest, which combines many decision trees, and working with both helped me understand why it is useful to try different algorithms instead of assuming that one will always perform best.

I also learned the importance of hyperparameter tuning. For Logistic Regression, I used GridSearchCV to test different values of `C` and selected the best setting based on macro F1. This showed me that performance changes with a model's settings, and that we should use cross-validation on the training data to choose them instead of relying on a single result.

I learned why accuracy alone is not enough to evaluate a model. Our classes have different sizes, so a model can perform well overall while struggling with one class. Precision, recall, F1-score, and the confusion matrix show these differences and which classes are confused with one another. A fair comparison also requires both models to use the same training and test sets and the same metrics; otherwise, differences might come from how the data was split or evaluated, not from the models.

One of the most important lessons was that a higher score does not automatically mean a model is the best choice. Since our goal is to help universities identify students at risk of dropping out, we need to pay particular attention to how well each model identifies the Dropout class, while also considering the other classes.

Finally, I learned that teamwork is essential in machine learning projects. Each member is responsible for a different part, but the parts must fit together, and discussing the findings as a team leads to a more reliable decision-support system. Machine learning is not only about writing code; it is also about making thoughtful decisions and understanding what the results mean.

---

## ساره الجبرين
*Model Evaluation & Comparison*

### What I Learned

My part was to evaluate and compare the Random Forest and Logistic Regression models. The main lesson was that accuracy alone is misleading when one class is small: *Enrolled* is only about 18% of the students, so I used macro F1 as the main metric and looked at precision, recall, and F1 for each class. The confusion matrices showed which classes get mixed up, mostly Graduate and Dropout students predicted as Enrolled. I also learned the difference between cross-validation on the training data and the final test set, and how to use a McNemar test to check whether an accuracy gap between two models could be just chance.

The *Enrolled* class was hard for both models, so I had to explain why it is weak and not only report the number. The Logistic Regression tuning also gave a different `C` on different machines because two values were almost tied, so I wrote the analysis so that it does not depend on one exact number. Combining my section with my teammates' work in one notebook without changing their code was another challenge. Next time, I would agree on library versions and on the shared evaluation function earlier, so the results are the same on every machine.

### Use of AI Tools

Claude (Anthropic) was used as a supporting tool to help verify parts of my work. I reviewed the content and checked the results myself, and I am responsible for their accuracy.