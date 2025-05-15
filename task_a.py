import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree


def main():
    # 1) Read CSV values in to dataframe to build our decision tree
    df = pd.read_csv("task_a_features.csv")
    
    # 2) Data Cleanup/Processing
    # TODO: How to deal with NULL values? Set to 0 for now, this might be incorrect for some attributes.
    df = df.fillna(0)
    X = df.drop(['playerID', 'class'], axis=1)
    y = df['class'] 
    
    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # Can adjust test size as a percentage of the data
    
    # Cross-validation strategy
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # 2) Build our decision tree
    model = DecisionTreeClassifier(criterion='entropy')
    
    # //TODO: Parameters to tune. Needs to be adjusted. min_samples_split and min_samples_leaf allow integer or fractional values
    param_grid = {'max_depth': [1, 2, 3, 4], 'min_samples_split': [2, 3, 5, 10, 25], 'min_samples_leaf': [1, 3, 5, 10, 25]}
    
    # Cross validation through GridSearchCV, 5 folds
    grid_model = GridSearchCV(estimator=model,
                          param_grid=param_grid,
                          scoring='f1', # TODO: Adjust based on accuracy, f1, precision, etc...
                          cv=skf,
                          verbose=2,
                          n_jobs=-1)

    # 3) Use our decision tree to predict results of data. Essentially testing the "goodness" of our decision tree 
    grid_model.fit(X_train, y_train)
    print("Best params found by grid search: ", grid_model.best_params_)
    print("Best score found by grid search: ", grid_model.best_score_)
    
    # feature_importances = grid_model.best_estimator_.feature_importances_
    # feature_importance_df = pd.DataFrame({
    #     'Feature': df.drop(['playerID', 'class'], axis=1).columns.tolist(),
    #     'Importance': feature_importances
    # }).sort_values(by='Importance', ascending=False)

    # print(feature_importance_df)
    
    
    y_pred = grid_model.best_estimator_.predict(X_test)
    print(classification_report(y_test,y_pred))

    # 4) Visualize results (decision tree and confusion_matrix)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=grid_model.best_estimator_.classes_)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix.png", dpi=500)
    plt.close()
    
    plt.figure(figsize=(20,8))
    plot_tree(grid_model.best_estimator_, fontsize=7)
    plt.savefig("tree_plot.png", dpi=300, bbox_inches='tight')
    print("CLF max depth of decision tree: ", grid_model.best_estimator_.max_depth)
    print("CLF minimum samples required to split an internal node: ", grid_model.best_estimator_.min_samples_split)
    print("CLF min number of samples required to be at a leaf nodes: ", grid_model.best_estimator_.min_samples_leaf)


if __name__ == "__main__": 
    main()