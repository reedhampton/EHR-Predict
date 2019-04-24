from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
import pandas as pd
import os
dirpath = os.getcwd()
'''
    The initial iteration issues:
        Encoding Categorical variables alters the "shape" of the
        dataframe drastically:
        let say you have dataframe A with categorical variable var1:
         index | var1 |                                     index | a | b
        -------------------- The encoding will change it to -----------------------
        1      |   a  |                                         1 | 1 | 0
        2      |   b  |                                         2 | 0 | 1
        
        So Until I perform the final clean on the master dataset, which will likely take several hours the input vector 
        for the current iteration will be very different from the finalized version: 
        However the input from the web-front end will not change: a csv file containing the hourly recorded measured
        vitals of the  individual. As such is the the case this will connect only one dummy variable, the functions 
        That needs to be changed are the ones pertaining to data transformation and not the ones that actually can a 
        model.
        
        Also the prediction will obviously be meaningly since the data is not scaled but worry not sklearn lets
        you save scaling factors.
        
'''

def place_holder_data_transformation(df):
    df = df.drop(columns=['subject_id', 'hadm_id', 'icustay_id', 'intime', 'icd9_code', 'gender', 'ethnicity',
                          'dob', 'admittime', 'dod', 'expire_flag', 'charttime', 'heart_rhythm'])
    df = df.mean(axis = 0)
    return df

def call_cloud_eval_with_model(X):
    PROJECT_ID = "ehrkeras"
    MODEL_NAME = "mortality_placeholder"
    CREDENTIALS_FILE = "/home/ec2-user/environment/EHR-Predict/lib/assets/credentials.json"

    list1 = []
    for x in X:
        list1.append(x)

    inputs_for_prediction = [
        {"input": list1}
    ]

    # Connect to the Google Cloud-ML Service
    credentials = GoogleCredentials.from_stream(CREDENTIALS_FILE)
    service = googleapiclient.discovery.build('ml', 'v1', credentials=credentials)

    # Connect to our Prediction Model
    name = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
    response = service.projects().predict(
        name=name,
        body={'instances': inputs_for_prediction}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    results = response['predictions']

    print(results)

    return results

def main():
    X = pd.read_csv("/home/ec2-user/environment/EHR-Predict/uploads/Patient Data.csv")

    X = (place_holder_data_transformation(X)).values
    results = call_cloud_eval_with_model(X)
    print("shape: ",X.shape)
    return results

if __name__ == "__main__":
    main()