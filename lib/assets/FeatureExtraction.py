import tsfresh.feature_extraction.feature_calculators as tffe
import pandas as pd
import numpy as np
from datetime import datetime
import machineL as ML
from sklearn.externals import joblib


def isNaN(x):
    return x != x

def is_same_day(time1, time2):
    if (time1.year != time2.year):
        return False
    else:
        if (time1.month != time2.month):
            return False
        else:
            if (time1.day != time2.day):
                return False
    return True

def scalar_feature_extraction(column):
    retval = np.zeros([1,10], dtype=float)
    retval[0][0] = tffe.count_above_mean(column.values)
    retval[0][1] = tffe.mean(column.values)
    retval[0][2] = tffe.maximum(column.values)
    retval[0][3] = tffe.median(column.values)
    retval[0][4] = tffe.minimum(column.values)
    retval[0][5] = tffe.sample_entropy(column.values)
    if(isNaN(retval[0][5])):
        retval[0][5] = 0
    retval[0][6] = tffe.skewness(column.values)
    retval[0][7] = tffe.variance(column.values)
    retval[0][8] = tffe.longest_strike_above_mean(column.values)
    retval[0][9] = tffe.longest_strike_below_mean(column.values)
    return retval

def logistic_feature_extraction(column):
    retval = np.zeros([1, 1], dtype=float)
    retval[0][0] = tffe.mean(column.values)
    return retval


def get_feature_date(daydf):
    daydf = daydf.drop("charttime", axis=1)
    daydf = daydf.drop("subject_id", axis=1)
    daydf = daydf.drop("icustay_id", axis=1)
    retval = np.zeros([1,0], dtype=float)
    retval = pd.DataFrame(retval)
    for column in daydf:
        #print(retval.shape)
        if((column == "heart_rate") | (column == "abp_systolic")
                | (column == "gcs_total") | (column == "platelets") | (column == "creatinine")):
            t = scalar_feature_extraction(daydf[column])
            t = pd.DataFrame(t)
            retval = pd.concat([retval, t], axis=1)
        elif((column == "weight") | (column == "age")):
            t = np.zeros([1,1], dtype=float)
            t[0][0] = daydf.iloc[0][0]
            t = pd.DataFrame(t)
            retval = pd.concat([retval, t], axis=1)
        elif(column == "is_dead_in_n_hours"):
            t = np.zeros([1,1], dtype=float)
            t[0][0] = tffe.maximum(daydf[column].values)
            t = pd.DataFrame(t)
            retval = pd.concat([retval, t], axis=1)
        else:
            t = logistic_feature_extraction(daydf[column])
            t = pd.DataFrame(t)
            retval = pd.concat([retval, t], axis=1)
    return retval

def daily_summary(df):
    print("entered df")
    col_names = df.columns.values
    new_df = pd.DataFrame(columns=col_names)
    interim_df = pd.DataFrame(columns=col_names)
    curr_icu_stay_id = df.iloc[0].loc['icustay_id']
    interim_index = 0
    try:
        curr_day = datetime.strptime(str(df.iloc[0].loc['charttime']), "%Y-%m-%d %H:%M:%S")
    except:
        curr_day = datetime.strptime(str(df.iloc[0].loc['charttime']), "%m/%d/%Y %H:%M")
    print("entering for loop")
    for index in range(len(df.index)):
        print("index: ", index)
        row_icu_stay_id = df.iloc[index].loc['icustay_id']
        try:
            row_day = datetime.strptime(str(df.iloc[index].loc['charttime']), "%Y-%m-%d %H:%M:%S")
        except:
            row_day = datetime.strptime(str(df.iloc[index].loc['charttime']), "%m/%d/%Y %H:%M")

        if ((row_icu_stay_id == curr_icu_stay_id) & (is_same_day(curr_day, row_day))):
            print("begin if")
            print(df.iloc[index].loc['charttime'])
            interim_df = interim_df.append(df.iloc[index], ignore_index=True)
            print("end if")
        else:
            new_row = get_feature_date(interim_df)
            curr_day = row_day
            curr_icu_stay_id = row_icu_stay_id
            if(interim_index == 0):
                new_df = pd.DataFrame(columns=new_row.columns.values)
            new_df = new_df.append(new_row, ignore_index=True)
            interim_df = pd.DataFrame(columns=col_names)
            interim_df = interim_df.append(df.iloc[index], ignore_index=True)
            print("completed day")
            interim_index = interim_index+1

    # print(new_df.head())
    new_row = get_feature_date(interim_df)
    new_df = new_df.append(new_row, ignore_index=True)
    return new_df

def single_day_summary(cleaned_file_name):
    df = pd.read_csv(cleaned_file_name, nrows=20)
    df = ML.add_age_column(df)
    df = ML.add_isdead_column(df)
    #print("completed calc age")
    df = df.drop(['intime', 'expire_flag', 'hadm_id', 'admittime'], axis=1)
    enc_df = pd.read_csv("enc_format.csv")
    col_vals = enc_df.columns.values
    size = len(df.index)
    #print(enc_df.values)
    ncol = len(enc_df.columns)
    for index in range(size):
        zero_row = np.zeros((1,ncol))
        zero_df = pd.DataFrame(zero_row, columns=col_vals)
        enc_df = enc_df.append(zero_df.iloc[0])
    #    print("zero_df shape: ", zero_df.shape)
    #    print("enc_df shape: ", enc_df.shape)

    for index in range(size):
        enc_df.iloc[index]['subject_id'] = df.iloc[index]['subject_id']
        enc_df.iloc[index]['icustay_id'] = df.iloc[index]['icustay_id']
        enc_df.iloc[index]['charttime'] = df.iloc[index]['charttime']
        enc_df.iloc[index]['heart_rate'] = df.iloc[index]['heart_rate']
        enc_df.iloc[index]['abp_systolic'] = df.iloc[index]['abp_systolic']
        enc_df.iloc[index]['gcs_total'] = df.iloc[index]['gcs_total']
        enc_df.iloc[index]['platelets'] = df.iloc[index]['platelets']
        enc_df.iloc[index]['creatinine'] = df.iloc[index]['creatinine']
        enc_df.iloc[index]['weight'] = df.iloc[index]['weight']
        enc_df.iloc[index]['category_' + str(df.iloc[index]['icd9_code'])] = 1
        enc_df.iloc[index]['category_' + str(df.iloc[index]['gender'])] = 1
        enc_df.iloc[index]['category_' + str(df.iloc[index]['ethnicity'])] = 1
        enc_df.iloc[index]['category_' + str(df.iloc[index]['heart_rhythm'])] = 1
        enc_df.iloc[index]['is_dead_in_n_hours'] = df.iloc[index]['is_dead_in_n_hours']

    #for index in range(size):
        #print(enc_df.iloc[index].values)

    #print("shape of df: ", df.shape, ", shape of enc: ", enc_df.shape)
    #for index in range(len(enc_df.columns)):
    #    print(enc_df.iloc[0].iloc[index])
    return enc_df


def file_to_features(cleaned_file_name):
    #this is the function to get the final evaluation data the data must be imputed at
    #this point
    df = single_day_summary(cleaned_file_name)
    df = get_feature_date(df)
    df = ML.row_correction(df)
    feature_scaler = joblib.load("feature_scaler.save")
    test_set = feature_scaler.transform(df.values)
    return test_set

def main():
    print("begin")
    df = pd.read_csv("master_table_fully_cleaned.csv", nrows=1000000)
    print("finish reading csv")
    df = df.drop(df.columns[0], axis=1)
    for column in df:
        print(column)
    print(df.iloc[[0]])
    data = daily_summary(df)
    print(data)
    data.to_csv("feature_data_up.csv", index=False)

    return 0

if __name__ == "__main__":
    main()