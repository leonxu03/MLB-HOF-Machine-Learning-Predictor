# MLB Hall of Fame Machine Learning Predictor
• ML model using scikit-learn to determine most influential stats predicting a player’s HOF probability

• Leveraged pandas and matplotlib libraries to visualize results in decision trees and confusion matrices

• Optimized model performance by tuning hyperparameters with K-Fold Cross Validation using GridSearchCV

### Project Setup

---

To begin, create a venv and install libraries from requirements.txt.

1. Create a venv with the following command.

```
python -m venv venv
or
python3 -m venv venv
```

2. Activate the virtual environment

```
source venv/bin/activate or \Scripts\activate
```

3. Install required dependencies

```
pip install -r requirements.txt
```

**DEPRECATED:** (Optional) The .ipynb file requires you to install extensions for Jupyter Notebook like usage.

---

### Key Ideas

---

Key ideas to focus on are grid search, training/test splits in the context of machine learning, tuning hyperparameters, decision tree classifiers. :)

---

### How to Use

---

Usage:
The original feature selection can be found in ECE356Lab4.sql. **DO NOT** modify this file.
If you do, you will need to update the CSV for any update you make to the task_a_features.sql or task_b_features.sql file.
Make changes in the above SQL files, and execute them in MySQLWorkbench. Export the rows returned as a CSV (you can overwrite to the ones in this repo).

Once you have updated the csv data, you can proceed with running the script.

To run the script for task A:

```
python3 task_a.py
```

To run the script for task B:

```
python3 task_b.py
```

Both will provide output in the terminals, specifically the best parameters that GridSearchCV has found along with the classification report.

The important scores to look out for are accuracy, precision, recall, f1-score (harmonic mean of precision and recall).
