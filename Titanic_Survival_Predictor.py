import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix


# ---------------------------------------------------------------------------
#   Function Name: DataLoad
#   Description :  Load the data from csv
#   Input :        Name of the csv file
#   Output :       DataFrame
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def DataLoad(filename):

    df = pd.read_csv(filename)

    print("Data Loaded Successfully")
    print(df.head())

    return df


# ---------------------------------------------------------------------------
#   Function Name: PreprocessData
#   Description :  It performs data preprocessing
#   Input :        DataFrame
#   Output :       Updated DataFrame
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def PreprocessData(df):

    # Remove unnecessary columns

    df = df.drop(
        ["Passengerid", "zero", "name"],
        axis=1,
        errors="ignore"
    )

    # Handle missing values

    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna(df["Age"].median())

    if "Fare" in df.columns:
        df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].fillna(
            df["Embarked"].mode()[0]
        )

    # Convert categorical data into numerical data

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    df = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=True,
        dtype=int
    )

    print("Data Preprocessing Completed")
    print(df.head())

    return df


# ---------------------------------------------------------------------------
#   Function Name: SplitData
#   Description :  It performs splitting activity
#   Input :        DataFrame
#   Output :       Training and testing data
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def SplitData(df):

    X = df.drop("Survived", axis=1)
    Y = df["Survived"]

    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
        random_state=42
    )

    print("Data Set Splitting Successfully")

    return X_train, X_test, Y_train, Y_test


# ---------------------------------------------------------------------------
#   Function Name: Trainmodel
#   Description :  It performs model training
#   Input :        Training Features and Target
#   Output :       Trained model
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def Trainmodel(X_train, Y_train):

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, Y_train)

    print("Model Trained Successfully")

    return model


# ---------------------------------------------------------------------------
#   Function Name: Evaluatemodel
#   Description :  It performs model testing
#   Input :        Model, testing features and testing target
#   Output :       None
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def Evaluatemodel(model, X_test, Y_test):

    Y_pred = model.predict(X_test)

    accuracy = accuracy_score(Y_test, Y_pred)

    print("Accuracy :", accuracy)

    print("Confusion Matrix :")
    print(confusion_matrix(Y_test, Y_pred))


# ---------------------------------------------------------------------------
#   Function Name: Preservemodel
#   Description :  It preserves model into .pkl file
#   Input :        Model and filename
#   Output :       None
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def Preservemodel(model, filename):

    joblib.dump(model, filename)

    print("Model Preserved With Name :", filename)


# ---------------------------------------------------------------------------
#   Function Name: Main
#   Description :  Entry Point Function
#   Input :        None
#   Output :       None
#   Author :       Omkar Dnyandev Shinde
#   Date :         16-08-2026
# ---------------------------------------------------------------------------

def main():

    # Step 1 : Load Data

    df = DataLoad("MarvellousTitanicDataset.csv")

    # Step 2 : Preprocess Data

    df = PreprocessData(df)

    # Step 3 : Split Data

    X_train, X_test, Y_train, Y_test = SplitData(df)

    # Step 4 : Train Model

    model = Trainmodel(X_train, Y_train)

    # Step 5 : Evaluate Model

    Evaluatemodel(model, X_test, Y_test)

    # Step 6 : Preserve Model

    Preservemodel(model, "MarvellousTitanic.pkl")


# ---------------------------------------------------------------------------
#   Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()