from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
import pandas as pd
import FeatureExtraction as FE
import os

dirpath = os.getcwd()

filename = dirpath + '/uploads/Patient Data.csv'

def call_cloud_eval_with_model(X, MODEL_NAME):
    PROJECT_ID = "ehrkeras"
    CREDENTIALS_FILE = dirpath + "/lib/assets/credentials.json"

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


    return results


def eval(filename):
    test_set = FE.file_to_features(filename)
    test_set = test_set[0]
    true_val = test_set[185]
    test_set = test_set[0:-1]

    MODEL_NAME_DNN = "dnnMortality"
    MODEL_NAME_L1NN = "l1nnMortality"
    MODEL_NAME_L2NN = "l2nnMortality"
    L1 = call_cloud_eval_with_model(test_set, MODEL_NAME_L1NN) #Worst
    L2 = call_cloud_eval_with_model(test_set, MODEL_NAME_L2NN) #Good
    DNN = call_cloud_eval_with_model(test_set, MODEL_NAME_DNN) #Best
    auroc_scores = pd.read_csv(dirpath + "/lib/assets/auc.csv")                               #AUC scores are precomputed
    
    #DNN: [{'is_dead': [0.12375179678201675]}]
    
    DNN_AUROC = auroc_scores['drop_auc'][0]
    L1_AUROC = auroc_scores['l1_auc'][0]
    L2_AUROC = auroc_scores['l2_auc'][0]
    
    DNNlist = DNN[0]
    for key in DNNlist.keys():
        DNN_Key = key;
        
    L1list = L1[0]
    for key in L1list.keys():
        L1_Key = key;
        
    L2list = L2[0]
    for key in L2list.keys():
        L2_Key = key;
        
    DNN_return = DNNlist[DNN_Key]
    L1_return = L1list[L1_Key]
    L2_return = L2list[L2_Key]
    return_list = [str(DNN_return)[1:-1], str(L1_return)[1:-1], str(L2_return)[1:-1], DNN_AUROC, L1_AUROC, L2_AUROC]
        
    return return_list

def main():
    string1 = eval(filename)
    print(string1)
    return

if __name__ == "__main__":
    main()