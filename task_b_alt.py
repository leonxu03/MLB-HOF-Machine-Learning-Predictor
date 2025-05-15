import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree


def main():
    # INITIAL MODEL
    # 1) Read CSV values in to dataframe to build our decision tree
    df = pd.read_csv("task_b_features.csv")
    
    # 2) Data Cleanup/Processing
    # TODO: How to deal with NULL values? Set to 0 for now, this might be incorrect for some attributes.
    df = df.fillna(0)
    X = df.drop(['playerID', 'class'], axis=1)
    y = df['class'] 
    
    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # Can adjust test size as a percentage of the data
    
    # 2) Build our decision tree classifier model
    model = DecisionTreeClassifier()
    
    # Cross-validation strategy
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='f1')
    print("Mean cross-validation f1:", scores.mean())
    
    model.fit(X_train, y_train)
    feature_importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': df.drop(['playerID', 'class'], axis=1).columns.tolist(),
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    print(feature_importance_df)
    
    # 3) Predict and evaluate model
    y_pred = model.predict(X_test)
    print("Initial Model Classification Report:")
    print(classification_report(y_test,y_pred))
    
    # 4) Visualize results (decision tree and confusion_matrix)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix_b_initial.png", dpi=500)
    plt.close()
    
    plt.figure(figsize=(20,14))
    plot_tree(model, feature_names=X.columns, class_names=y.unique().astype(str), fontsize=3)
    plt.savefig("tree_plot_b_initial.svg", format="svg") # Needs to be viewed in a web browser
    plt.close()
    
    # ALTERNATIVE MODEL
    
    print("\nProceeding with GridSearch for Hyperparameter Tuning...\n")
    
    # 5) Grid Search Cross Validation
    alt_model = DecisionTreeClassifier()
    # //TODO: Parameters to tune. Needs to be adjusted. min_samples_split and min_samples_leaf allow integer or fractional values
    param_grid = {'max_depth': [1, 2, 3, 4], 'min_samples_split': [2, 3, 5, 10, 25], 'min_samples_leaf': [1, 3, 5, 7, 10, 25]}

    # Cross validation through GridSearchCV, 5 folds
    grid_model = GridSearchCV(estimator=alt_model,
                          param_grid=param_grid,
                          scoring='f1', # TODO: Adjust based on accuracy, f1, precision, etc...
                          cv=skf,
                          verbose=0,
                          n_jobs=-1)

    # 6) Use our decision tree to predict results of data. Essentially testing the "goodness" of our decision tree 
    grid_model.fit(X_train, y_train)
    print("Best params found by grid search: ", grid_model.best_params_)
    # print("Best score found by grid search: ", grid_model.best_score_)
    
    feature_importances = grid_model.best_estimator_.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': df.drop(['playerID', 'class'], axis=1).columns.tolist(),
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    print(feature_importance_df)
    
    y_pred_alt = grid_model.best_estimator_.predict(X_test)
    print("Alternative Model Classification Report:")
    print(classification_report(y_test,y_pred_alt))

    # 7) Visualize results (decision tree and confusion_matrix)
    cm = confusion_matrix(y_test, y_pred_alt)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=grid_model.best_estimator_.classes_)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix_b_alt.png", dpi=500)
    plt.close()
    
    plt.figure(figsize=(20,8))
    plot_tree(grid_model.best_estimator_, feature_names=X.columns, class_names=y.unique().astype(str),fontsize=7)
    plt.savefig("tree_plot_b_alt.png", dpi=300, bbox_inches='tight')
    print("CLF max depth of decision tree: ", grid_model.best_estimator_.max_depth)
    print("CLF minimum samples required to split an internal node: ", grid_model.best_estimator_.min_samples_split)
    print("CLF min number of samples required to be at a leaf nodes: ", grid_model.best_estimator_.min_samples_leaf)

    # FINAL MODEL

    # 8) Remove features that have an importance value of 0
    feature_to_remove = feature_importance_df[feature_importance_df['Importance'] == 0]
    print("\nRemoving following features:")
    for feature in feature_to_remove['Feature']:
        print(feature)
        X = X.drop(feature, axis=1)
        
    # 9) Redo Train Test Split on Modified Features
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
        
    final_model = DecisionTreeClassifier()
    final_grid = GridSearchCV(estimator=final_model,
                          param_grid=param_grid,
                          scoring='f1',
                          cv=skf,
                          verbose=0,
                          n_jobs=-1)
    
    # 10) Use our decision tree to predict results of data. Essentially testing the "goodness" of our decision tree 
    final_grid.fit(X_train, y_train)
    print("Best params found by grid search: ", final_grid.best_params_)
    # print("Best score found by grid search: ", final_grid.best_score_)
    
    feature_importances = final_grid.best_estimator_.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': X.columns.tolist(),
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    print(feature_importance_df)
    
    y_pred_final = final_grid.best_estimator_.predict(X_test)
    print("Final Model Classification Report:")
    print(classification_report(y_test,y_pred_final))

    # 11) Visualize results (decision tree and confusion_matrix)
    cm = confusion_matrix(y_test, y_pred_final)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=final_grid.best_estimator_.classes_)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix_b_final.png", dpi=500)
    plt.close()
    
    plt.figure(figsize=(20,8))
    class_names = y.unique().astype(str)
    plot_tree(final_grid.best_estimator_, feature_names=X.columns, class_names=class_names, fontsize=7)
    plt.savefig("tree_plot_b_final.png", dpi=300, bbox_inches='tight')
    print("Final model max depth of decision tree: ", final_grid.best_estimator_.max_depth)
    print("Final model minimum samples required to split an internal node: ", final_grid.best_estimator_.min_samples_split)
    print("Final model min number of samples required to be at a leaf nodes: ", final_grid.best_estimator_.min_samples_leaf)

    
if __name__ == "__main__": 
    main()