import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Load the trained model
def CheckIfFraud(datapath ='aml_2.csv'):
    
    model = joblib.load("aml_final.pkl")

    # Load the dataset
    datapd = pd.read_csv(
        datapath
    ).iloc[:5000]
    
    
    # Preprocessing steps (similar to what you've done before)
    col = [
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
    ]
    features = datapd[col]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    scaled_features = pd.DataFrame(scaled_features, columns=col)

    data_encode = datapd["type"]
    dummy = pd.get_dummies(data_encode, drop_first=True)
    data_fraud = datapd["isFraud"]

    dt = datapd.copy()
    cols = ["nameOrig", "nameDest"]
    dt[cols] = dt[cols].astype("category")
    for i in cols:
        dt[i] = dt[i].cat.codes
    know = dt[["nameOrig", "nameDest"]]

    flagged = datapd["isFlaggedFraud"]

    new_datapd = pd.concat([dummy, know, scaled_features, flagged], axis=1)

    col1 = ["nameOrig", "nameDest"]
    features1 = new_datapd[col1]
    scaler1 = StandardScaler()
    features1 = scaler1.fit_transform(features1)
    know1 = pd.DataFrame(features1, columns=col1)

    new_datapd["nameOrig"] = know1["nameOrig"]
    new_datapd["nameDest"] = know1["nameDest"]

    # Assuming 'isFraud' is the target column
    # Splitting the data into features and target
    x_test = new_datapd
    y_test = data_fraud

    # Make predictions and print details for each row
    for idx, row in datapd.iterrows():
        prediction = model.predict(x_test.iloc[idx: idx + 1])
        if prediction == 1:
            yield row[:-2]

