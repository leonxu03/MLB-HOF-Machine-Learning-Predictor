# MLB Hall of Fame Machine Learning Predictor
• ML model using scikit-learn to determine most influential stats predicting a player’s HOF probability

• Leveraged pandas and matplotlib libraries to visualize results in decision trees and confusion matrices

• Optimized model performance by tuning hyperparameters with K-Fold Cross Validation using GridSearchCV

### Results

---
#### Task A

> Part 1 - Initial Feature Selection (No Hyperparameter Tuning)
>
> <img width="663" alt="Screenshot 2025-05-14 at 10 50 00 PM" src="https://github.com/user-attachments/assets/037fcd02-ec0b-4779-9c23-61e3c525893b" />
>
> Part 2 - Initial Feature Selection (Hyperparameter Tuning)
>
> <img width="590" alt="Screenshot 2025-05-14 at 10 52 31 PM" src="https://github.com/user-attachments/assets/3c66f9f3-5bbe-4f82-b79b-e612710b6a29" />
>
> Part 3 - With Feature Removal (Hyperparameter Tuning)
>
> <img width="602" alt="Screenshot 2025-05-14 at 10 53 14 PM" src="https://github.com/user-attachments/assets/84ebfa0f-8833-4989-ab38-09d78a8a4664" />

#### Task B 

> Part 1 - Initial Feature Selection (No Hyperparameter Tuning)
> 
> <img width="669" alt="Screenshot 2025-05-14 at 10 51 35 PM" src="https://github.com/user-attachments/assets/20910706-e32f-40ba-a26a-e098b1c8e891" />
>
> Part 2 - Initial Feature Selection (Hyperparameter Tuning)
>
> <img width="621" alt="Screenshot 2025-05-14 at 10 56 06 PM" src="https://github.com/user-attachments/assets/33f17640-02b4-4440-9f0c-632cf05f7177" />
>
> Part 3 - With Feature Removal (Hyperparameter Tuning)
>
> <img width="667" alt="Screenshot 2025-05-14 at 10 56 35 PM" src="https://github.com/user-attachments/assets/564446b4-6ab3-4bac-b53e-aa7a342d6cec" />

---

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
