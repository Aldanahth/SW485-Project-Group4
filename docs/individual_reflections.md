# Individual Reflections

Each team member reflects below on what she learned and the challenges she faced during Phase 1.

---

## الدانة ال ثنيان

_Data Inspection & Repository Management_

### What I Learned

I learned that understanding the dataset is an important first step before starting any analysis. I used Python to check the number of rows and columns, the data types, and basic statistics, which gave me a clear idea of what the dataset contains and how it is organized.

I also learned how to check for missing values and visualize them. Even though our dataset had no missing values, I understood why this step is necessary before working with the data, and creating the chart helped me practice presenting information in a way that is easy to understand.

Analyzing the target class distribution showed me that Graduate is the largest class and Enrolled is the smallest. This made me realize that the classes are imbalanced and that we should keep this in mind when evaluating our models.

Working with GitHub also developed my existing skills. Although I had used it before, this project gave me more experience in organizing a repository, managing project files, and updating the README for the team. I also became more comfortable using Google Colab, running code cells in the correct order, and saving notebooks with their results.

Overall, this project improved my Python skills and helped me understand the importance of data inspection, clear documentation, and teamwork. I feel more confident working with datasets and managing my contribution to a group project.

### Challenges I Faced

One challenge was making sure that the notebook ran correctly and that all the results were saved after making changes. I also needed to keep the GitHub repository organized and make sure the README matched the project files. These experiences helped me become more careful when reviewing my work and managing updates.

---

## يسرى ال هلال

_Exploratory Data Analysis_

### What I Learned

Before this project, I thought that if a column contained numbers, I could simply treat it as a number. I learned that some columns, such as Course, use numbers only as labels, so I now check what each column really means before working with it.

I also learned that not every method works in every case. At first, I used correlation with the target, but a teammate explained that it does not work well when the target is made of categories. That is when I learned about mutual information and why it was a better choice here.

Working on the charts taught me how to read them and not only how to make them. I learned to ask what each chart is really showing and to describe it in simple words, using real numbers from the data. I also learned to be careful with my wording: two things appearing together does not mean that one causes the other, so I use "associated with" instead of saying that something causes dropout.

The prediction-timing issue made me think about how the system would work in real life. A model can look very good, but if it uses information we do not have yet, it is not useful.

Finally, I learned how helpful teamwork can be. My teammates found mistakes that I had not noticed, and fixing them made our work much better.

### Challenges I Faced

1. **Identifying the real type of each feature:** At first, all columns looked numeric, but many of them, such as `Course` and `Application mode`, are codes for categories. I had to separate the features into continuous, binary, and categorical groups and choose a suitable chart for each group.

2. **Measuring the relationship with a multi-class target:** In my first version, I encoded the target as 0, 1, and 2 and included it in the correlation heatmap. During the review, a teammate pointed out that Pearson correlation assumes equal distances between values, which is not true for outcome categories. I removed the target from the heatmap and used mutual information, box plots, and proportion charts instead.

3. **Loading the data correctly:** The file uses semicolons instead of commas, and the column name `Daytime/evening attendance` contains a trailing tab character, so I had to set the separator explicitly and clean the column names.

4. **Writing observations that match the data:** Some of my first observations were based on patterns I expected to see. After running the code on the real data, I found that some of them were not accurate, such as the difference for displaced students and the interpretation of zero grades. I corrected them and added the actual numbers.

5. **Avoiding cause-and-effect claims:** Some of my early wording suggested that features cause dropout. I rewrote the observations to describe associations only.

6. **Prediction timing:** The features most associated with the outcome (semester grades) are not available when a student first enrolls, which conflicts with the goal of early identification. I raised this with the team, and we decided to predict after the 1st semester.

---

## نجد الغانم

_Data Preprocessing_

### What I Learned

I learned how to decide which data a model should use, and that every choice is a trade-off. Our system is meant to help academic advisors warn students early. The dataset records six results for each of the two semesters: credited, enrolled, evaluated, and approved units, the grade, and units without evaluation. The second-semester results would make the model more accurate, but they only exist after the second semester ends, which is too late for an early warning. As a team, we compared the options, decided not to use the second-semester data, and chose to warn the advisor at the end of the first semester. I then cleaned the data to match that decision.

I also learned how to adapt when the data does not match the plan. The suggested dashboard includes GPA and attendance sliders, but when I checked the column names, I found that the dataset has no attendance column. I proposed to my teammates that we use what the data already has, and we agreed on an academic progress measure: approved units divided by enrolled units. While preparing it, an AI tool inspected the data and found a special case: 180 students enrolled in zero units, which makes the division impossible, and it helped us flag them. It also gave me a brief on the order of the steps, which showed me that cleaning data is a series of decisions. As a beginner, I ran every step myself and checked each output.

Finally, I learned that a number does not always mean a quantity. Codes such as Course are labels, not measurements, so they need different handling from real numbers.

### Challenges I Faced

One challenge was deciding which features were available at the first-semester prediction point, since second-semester information could not be used. I also had to handle students with zero enrolled units when calculating academic progress. Making sure that encoding, scaling, and other preprocessing steps used training data only helped me understand how to prevent data leakage.

---

## اريام الركيان

_Random Forest Model_

### What I Learned

Before this project, I thought that training a machine learning model was simply a matter of running a few lines of code with default settings. I learned that proper hyperparameter tuning with GridSearchCV, and choosing the right evaluation metric, such as macro F1 instead of basic accuracy, is essential for measuring the performance of all classes fairly, especially when predicting multi-class student outcomes like Dropout, Enrolled, and Graduate.

I also learned to look much more closely at the structure of the preprocessed dataset. A teammate pointed out that the split column should only be used to separate the training and testing sets and not be treated as a feature. This reminded me how important it is to coordinate with the team and understand every column in the data pipeline to avoid errors.

Working on the feature importance plot helped me understand how to interpret what the model is actually learning, and not only how to generate charts. I learned to analyze which demographic and academic factors drive the Random Forest predictions.

I also learned how important version control and clean collaboration are. Managing Jupyter notebooks and updating code on GitHub taught me to keep the repository structured and consistent for everyone.

Finally, I learned how valuable teamwork and code alignment can be. Discussing our approach with teammates helped us catch small pipeline details early and made our final modeling phase more robust.

### Challenges I Faced

Choosing hyperparameters was challenging because testing more combinations increased the training time, while several settings gave very similar scores. Predicting the Enrolled class was also difficult even after tuning. These results taught me to look beyond overall accuracy and interpret model performance carefully.

---

## جمانة العنزي

_Second Classification Model_

### What I Learned

Before this project, I thought that building a machine learning model was mostly about choosing an algorithm, training it, and checking its accuracy. I learned that there is much more to it, especially when predicting student outcomes across three classes: Dropout, Enrolled, and Graduate.

I learned that different models approach prediction differently. Logistic Regression works differently from Random Forest, which combines many decision trees, and working with both helped me understand why it is useful to try different algorithms instead of assuming that one will always perform best.

I also learned the importance of hyperparameter tuning. For Logistic Regression, I used GridSearchCV to test different values of `C` and selected the best setting based on macro F1. This showed me that performance changes with a model's settings, and that we should use cross-validation on the training data to choose them instead of relying on a single result.

I learned why accuracy alone is not enough to evaluate a model. Our classes have different sizes, so a model can perform well overall while struggling with one class. Precision, recall, F1-score, and the confusion matrix show these differences and which classes are confused with one another. A fair comparison also requires both models to use the same training and test sets and the same metrics; otherwise, differences might come from how the data was split or evaluated, not from the models.

One of the most important lessons was that a higher score does not automatically mean a model is the best choice. Since our goal is to help universities identify students at risk of dropping out, we need to pay particular attention to how well each model identifies the Dropout class, while also considering the other classes.

Finally, I learned that teamwork is essential in machine learning projects. Each member is responsible for a different part, but the parts must fit together, and discussing the findings as a team leads to a more reliable decision-support system. Machine learning is not only about writing code; it is also about making thoughtful decisions and understanding what the results mean.

### Challenges I Faced

One challenge was choosing a regularization setting because different values of C produced almost the same cross-validation scores. I also had to use the same preprocessed data and train/test split as Random Forest to keep the comparison fair. Balancing precision and recall for the Enrolled class helped me understand the trade-offs between evaluation metrics.

---

## ساره الجبرين

_Model Evaluation & Comparison_

### What I Learned

My part was to evaluate and compare the Random Forest and Logistic Regression models. The main lesson was that accuracy alone is misleading when one class is small: _Enrolled_ is only about 18% of the students, so I used macro F1 as the main metric and looked at precision, recall, and F1 for each class. The confusion matrices showed which classes get mixed up, mostly Graduate and Dropout students predicted as Enrolled. I also learned the difference between cross-validation on the training data and the final test set, and how to use a McNemar test to check whether an accuracy gap between two models could be just chance.

The _Enrolled_ class was hard for both models, so I had to explain why it is weak and not only report the number. The Logistic Regression tuning also gave a different `C` on different machines because two values were almost tied, so I wrote the analysis so that it does not depend on one exact number. Combining my section with my teammates' work in one notebook without changing their code was another challenge. Next time, I would agree on library versions and on the shared evaluation function earlier, so the results are the same on every machine.

### Use of AI Tools

Claude (Anthropic) was used as a supporting tool to help verify parts of my work. I reviewed the content and checked the results myself, and I am responsible for their accuracy.