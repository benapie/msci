import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix


def load_data():
    """
    Loads assessments.csv, studentAssessment.csv, and studentInfo.csv
    from the data folder and returns a dictionary containing
    panda dataframes.
    :return: Dictinoary of panda dataframes.
    """
    assessments = pd.read_csv("data/assessments.csv")
    student_assessment = pd.read_csv("data/studentAssessment.csv")
    student_info = pd.read_csv("data/studentInfo.csv")
    return {
        "assessment": assessments,
        "student_assessment": student_assessment,
        "student_info": student_info
    }


def initial_processing(input_data):
    """
    The prepreprocessing before we start cleaning the data.
    This function merges student_assessment and assessment
    together, calculated the custom attributed weight_score,
    merges the student_info table,
    and then converts the categorical labels to numerical.
    :param input_data: initial data.
    :return: processed data.
    """
    # Merging student_assessment and assessment
    new_data = pd.merge(
        input_data["student_assessment"][["id_student", "id_assessment", "score"]],
        input_data["assessment"][["id_assessment", "weight", "code_module", "code_presentation"]],
        on="id_assessment",
        how="left"
    )

    # Calculating weighted_score attribute
    new_data["weighted_score"] = new_data["weight"] * new_data["score"] * 0.01
    new_data = new_data[["id_student", "code_module", "code_presentation", "weighted_score"]]
    new_data = new_data.groupby(["id_student", "code_module", "code_presentation"], as_index=False).sum()

    # Adding student demographics
    new_data = pd.merge(
        new_data,
        input_data["student_info"],
        on=["id_student", "code_module", "code_presentation"]
    )

    # Making the labels numeric
    new_data.loc[new_data["final_result"] == "Withdrawn", "final_result"] = 0
    new_data.loc[new_data["final_result"] == "Fail", "final_result"] = 1
    new_data.loc[new_data["final_result"] == "Pass", "final_result"] = 2
    new_data.loc[new_data["final_result"] == "Distinction", "final_result"] = 3

    return new_data


def split_labels(input_data):
    """
    Splits the final_result from the input_data and returns it as a
    separate panda df.
    :param input_data: the input data.
    :return: data, data_labels.
    """
    input_data_labels = data["final_result"]
    input_data = data.drop("final_result", axis=1)
    return input_data, input_data_labels


def stratified_sample(input_data, input_data_labels):
    """
    Stratified sampling function.
    :param input_data: the input data.
    :param input_data_labels: the input data labels.
    :return: the training set, the training set labels, the test set, and the test set labels.
    """
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    new_train_set = None
    new_train_set_labels = None
    new_test_set = None
    new_test_set_labels = None

    for train_index, test_index in split.split(input_data, input_data_labels):
        new_train_set = input_data.loc[train_index]
        new_train_set_labels = input_data_labels.loc[train_index]
        new_test_set = input_data.loc[test_index]
        new_test_set_labels = input_data_labels.loc[test_index]

    return new_train_set, new_train_set_labels, new_test_set, new_test_set_labels


def display_scores(scores):
    print("Scores", scores)
    print("Mean", scores.mean())
    print("Standard deviation", scores.std())


# Data preparation
raw_data = load_data()
data = initial_processing(raw_data)
data, data_labels = split_labels(data)
train_set, train_set_labels, test_set, test_set_labels = stratified_sample(data, data_labels)

data.info()

# Constructing our pipeline for data processing
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),  # Median imputer
    ("std_scaler", StandardScaler())  # Standard scaler
])

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, list(data.iloc[:, [3, 9, 10]])),  # Numerical pipeline
    ("cat", OneHotEncoder(), list(data.iloc[:, [1, 2, 4, 8, 11]]))  # Categorical pipeline (one hot encoding)
])

# Transform train and test sets
train_set_prepared = full_pipeline.fit_transform(train_set)
test_set_prepared = full_pipeline.fit_transform(test_set)


# Train and fit data with selected parameters
logit_regression = LogisticRegression(max_iter=1000, C=100)
logit_regression.fit(train_set_prepared, train_set_labels.astype(int))
forest_regressor = RandomForestRegressor(n_estimators=90)
forest_regressor.fit(train_set_prepared, train_set_labels)

# Calculating prediction on the test set
forest_test_prediction = forest_regressor.predict(test_set_prepared)
logit_test_prediction = logit_regression.predict(test_set_prepared)

# Mean squared error calculations
forest_mse = mean_squared_error(forest_test_prediction, test_set_labels)
logit_mse = mean_squared_error(logit_test_prediction, test_set_labels)
print("Forest MSE", np.sqrt(forest_mse))
print("Logit MSE", np.sqrt(logit_mse))


