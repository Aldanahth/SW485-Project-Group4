# Team Meeting Notes

**Course:** SWE485  
**Project:** University Student Retention & Advisory Dashboard  
**Group:** 4  
**Phase:** Phase 1 — Data Exploration and Supervised Learning

## Meeting 1 — Data Exploration and Preprocessing

**Date:** October 15, 2026  
**Participants:** Aldanah, Najd, Yusra

### Topics Discussed
- Reviewed the dataset structure, class distribution, and exploratory analysis.
- Discussed data preprocessing and feature preparation.
- Reviewed the decision to use first-semester information for early prediction.
- Discussed excluding second-semester features because they are not available at the chosen prediction point.

### Decisions and Action Items
- **Team decision:** Predict student outcomes after the 1st semester, using enrollment-time and 1st semester features (30 of the original 36 features) and excluding the six 2nd semester features.
- **Team decision:** Use `academic_progress` (approved units divided by enrolled units) as an academic progress measure, because the dataset has no attendance column.
- **Najd:** Finalize and share the preprocessed dataset.
- **Yusra:** Complete exploratory data analysis and visualizations.
- **Aldanah:** Review dataset information and organize the GitHub repository documentation.

## Meeting 2 — Model Development

**Date:** October 19, 2026  
**Participants:** Aryam, Jumana, Najd

### Topics Discussed
- Reviewed the prepared dataset and shared training/testing split.
- Discussed Random Forest and Logistic Regression implementation.
- Compared baseline models with hyperparameter-tuned configurations.
- Reviewed cross-validation and model evaluation settings.

### Decisions and Action Items
- **Aryam:** Finalize Random Forest training and hyperparameter tuning.
- **Jumana:** Finalize Logistic Regression training and hyperparameter tuning.
- **Najd:** Support verification of preprocessing consistency.

## Meeting 3 — Model Evaluation and Documentation

**Date:** October 20, 2026  
**Participants:** Sarah, Aryam, Jumana, Aldanah

### Topics Discussed
- Compared model performance using accuracy, precision, recall, and F1-score.
- Reviewed confusion matrices and the challenges of predicting the Enrolled class.
- Discussed the final model comparison and selection.
- Reviewed evaluation results, visualizations, and documentation requirements.

### Decisions and Action Items
- **Sarah:** Finalize evaluation tables, plots, and results documentation.
- **Aryam and Jumana:** Verify model outputs and evaluation results.
- **Aldanah:** Review README documentation and repository organization.

## Meeting 4 — Final Group Review

**Date:** October 23, 2026  
**Participants:** Aldanah, Najd, Yusra, Aryam, Jumana, Sarah

### Topics Discussed
- Reviewed the Phase 1 deliverables and instructor requirements.
- Checked the Data Exploration and Supervised Learning notebooks.
- Reviewed saved models, evaluation results, and visualizations.
- Checked task distribution, individual reflections, and peer reviews.
- Reviewed the README, dependencies, and final repository structure.
- Discussed final corrections before the submission deadline.

### Decisions and Action Items
- Ensure all required files are included in the GitHub repository.
- Correct any remaining inconsistencies in the notebooks and documentation.
- Verify that the latest versions of all project files are uploaded.
- Complete the final submission by October 24, 2026.