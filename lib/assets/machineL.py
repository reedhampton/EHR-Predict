import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import *
from keras.utils import to_categorical
import tensorflow as tf
from sklearn import metrics
from sklearn import preprocessing
from sklearn.externals import joblib
from datetime import datetime
import tsfresh.feature_extraction.feature_calculators as tffe

def calc_auroc(model, test_df):
    true_vals = test_df[185].values
    test_df = test_df.drop(185, axis = 1)
    pred_vals = np.array([], dtype=np.float)
    for index in range(len(test_df.index)):
        col_names = test_df.columns.values
        df_pred = pd.DataFrame(columns=col_names)
        df_pred = df_pred.append(test_df.iloc[index])
        pred = model.predict(np.array(df_pred.values))
        inter_np = np.array(pred, dtype=np.float)
        pred_vals = np.append(pred_vals, inter_np)
    auc = metrics.roc_auc_score(y_true=true_vals, y_score=pred_vals)
    print("auc score is: ", auc)
    return auc

#--------------post-preprocessing-processing code-------------------------------------------

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


def is_same_hour(time1, time2):
    if (time1.year != time2.year):
        return False
    else:
        if (time1.month != time2.month):
            return False
        else:
            if (time1.day != time2.day):
                return False
            else:
                if(time1.hour != time2.hour):
                    return False
    return True


def significantTimeDifference(time1, time2, diff): #diff being hours
    if(time2 - time1).total_seconds() <= diff*60*60:
        return True
    return False


def add_age_column(df):
    age_col = pd.DataFrame(np.zeros((df.shape[0], 1)), columns=['age'])
    for index, row in df.iterrows():
        try:
            charttime = datetime.strptime(str(row['charttime']), "%Y-%m-%d %H:%M:%S")
            dob = datetime.strptime(str(row['dob']), "%Y-%m-%d %H:%M:%S")
        except:
            charttime = datetime.strptime(str(row['charttime']), "%m/%d/%Y %H:%M")
            dob = datetime.strptime(str(row['dob']), "%m/%d/%Y %H:%M")
        age_val = charttime.year - dob.year
        age_col.iloc[index] = age_val
        #age_col = age_col.append({'age': age_val}, ignore_index=True)
        #print("Age progression: ", age_val, ", line: ", index)

    df = pd.concat([df, age_col], axis=1)
    df = df.drop(['dob'], axis=1)
    return df

def add_isdead_column(df): #n denoted in hours
    dead_col = pd.DataFrame(np.zeros((df.shape[0],1)),columns=['is_dead_in_n_hours'])
    for index, row in df.iterrows():
        if(isNaN(row['dod'])):
            dead_col.iloc[index] = 0

        else:
            try:
                charttime = datetime.strptime(str(row['charttime']), "%Y-%m-%d %H:%M:%S")
                dod = datetime.strptime(str(row['dod']), "%Y-%m-%d %H:%M:%S")
            except:
                charttime = datetime.strptime(str(row['charttime']), "%m/%d/%Y %H:%M")
                dod = datetime.strptime(str(row['dod']), "%m/%d/%Y %H:%M")

            dead_in_n = significantTimeDifference(charttime, dod, 24)
            if(dead_in_n):
                dead_in_n = 1
            else:
                dead_in_n = 0
            dead_col.iloc[index] = dead_in_n

    df = pd.concat([df, dead_col], axis=1)
    df = df.drop(['dod'], axis=1)
    return df

def is_categorical(df_col):
    return df_col.dtype.name == 'category'

def one_hot_encode_df_single_column(df, column):
    '''
    :param df: dataframe
    :param column: string - name of cloumn
    :return:
    '''
    df[column] = pd.Categorical(df[column])
    hot_encoded_col = pd.get_dummies(df[column], prefix='category')
    df = pd.concat([df, hot_encoded_col], axis=1)
    df = df.drop(columns=[column])
    return df

def get_daily_summary(df):
    # ----------------------------------NEEED DONE - TSFRESH--------------------------------------------
    return True


def translate_to_hourly(df):
    col_names = df.columns.values
    new_df = pd.DataFrame(columns=col_names)
    interim_df = pd.DataFrame(columns=col_names)
    curr_icu_stay_id = df.iloc[0].loc['icustay_id']
    curr_hour = datetime.strptime(str(df.iloc[0].loc['charttime']), "%Y-%m-%d %H:%M:%S")
    for index in range(len(df.index)):
        print("index: ", index)
        row_icu_stay_id = df.iloc[index].loc['icustay_id']
        row_hour = datetime.strptime(str(df.iloc[index].loc['charttime']), "%Y-%m-%d %H:%M:%S")

        if ((row_icu_stay_id == curr_icu_stay_id) & (is_same_hour(curr_hour, row_hour))):
            print(df.iloc[index].loc['charttime'])
            interim_df = interim_df.append(df.iloc[index], ignore_index=True)
        else:
            new_row = interim_df.mean(axis = 0)
            new_row.loc['charttime'] = curr_hour.strftime("%Y-%m-%d %H:%M:%S")
            new_row.loc['is_dead_in_n_hours'] = tffe.maximum(interim_df['is_dead_in_n_hours'].values)
            curr_hour = row_hour
            curr_icu_stay_id = row_icu_stay_id
            new_df = new_df.append(new_row, ignore_index=True)
            interim_df = pd.DataFrame(columns=col_names)
            interim_df = interim_df.append(df.iloc[index], ignore_index=True)
            print("completed hour")

            ''' # commented stuff used during testing
            print("-----------------------------------------------------------------")
            print("average: \n", new_row)
            print("end of average")
            for index, row in interim_df.iterrows():
                print(row)
            #x = input("Pause:")'''

    #print(new_df.head())
    new_row = interim_df.mean(axis=0)
    new_row.loc['charttime'] = curr_hour.strftime("%Y-%m-%d %H:%M:%S")
    new_df = new_df.append(new_row, ignore_index=True)

    return new_df


def final_clean(df):  # function specific to mimic
    df = add_age_column(df)
    print("completed calc age")
    df = df.drop(['intime', 'expire_flag', 'hadm_id', 'admittime'], axis = 1)
    df = one_hot_encode_df_single_column(df, 'icd9_code')
    print("completed icd9 encoding")
    df = one_hot_encode_df_single_column(df, 'gender')
    print("completed gender encoding")
    df = one_hot_encode_df_single_column(df, 'ethnicity')
    print("completed ethnicity encoding")
    df = one_hot_encode_df_single_column(df, 'heart_rhythm')
    print("completed heartrhtyhm enc")
    #df = add_age_column(df)
    #print("completed calc age")
    df = add_isdead_column(df)
    print("completed calc death")
    df = translate_to_hourly(df)
    print("completed hourly translation")
    return df

#-------------------------End of Post Preprocessing Codes---------------------------------------------
#-----------------------------Models------------------------------------------------------------------
'''
    When the model maker is called: preprocessing including one-hot encoding for the data must be completed
    Except for scaling
    AdaBoost/ Random Forest - uses Sklearn, Gradient Boost to be implemented using XGboost
'''
#----------------------Makeshift fc Neural Net------------------------------------------------------------
#-------daily summarized daily: scalar: mean, categorical: proportion---------------------------------


def mk_fcnn(num_layers, num_neuron_per_layer, hidden_act_funct, df_train, df_test, target_col_name, num_possible_outcomes,
            bch_sz, is_dropout = False, droprate = 0.5, is_l1 = False, l1rate = 0.01, is_l2 = False, l2rate = 0.01, categ_target=False):
    '''
    :param num_layers:  1-5
    :param num_neuron_per_layer: 50 - 500 - should be inversely correlated with the number of layers
    :param hidden_act_funct:  relu / elo / sigmoid
    :param df_train: training dataframe
    :param df_test: test dataframe
    :param target_col_name:
    :param num_possible_outcomes:
    :param bch_sz: batch size
    :param is_dropout: Boolean
    :param droprate: Percentage of neurons to drop at that layer
    :param is_l1: Boolean
    :param l1rate: 0.01 - 0.03
    :param is_l2: Boolean
    :param l2rate: 0.01 - 0.03
    :return:
    '''

    print(df_train.shape, ", ", df_test.shape)

    X_train = df_train.drop(target_col_name, axis = 1).values
    Y_train = df_train[[target_col_name]].values
    X_test = df_test.drop(target_col_name, axis=1).values
    Y_test = df_test[[target_col_name]].values
    activationsl = 'linear'
    lossl = 'mse'
    opt1 = 'adam'
    if(categ_target):
        Y_test = to_categorical(Y_test)
        Y_train = to_categorical(Y_train)
        num_possible_outcomes = num_possible_outcomes+1
        activationsl = 'softmax'
        lossl = 'categorical_crossentropy'
        opt1 = 'adadelta'
    '''
    Y_test = pd.Categorical(df_test['is_dead_in_n_hours'])
    Y_test = pd.get_dummies(Y_test, prefix='category')
    Y_train = pd.Categorical(df_train['is_dead_in_n_hours'])
    Y_train = pd.get_dummies(Y_train, prefix='category')
    '''

    #print(df_train.columns)
    print(X_test.shape)


    #Normal
    input_layer = Dense(num_neuron_per_layer, input_dim=len(df_train.columns)-1, activation=hidden_act_funct)
    hidden_layer = Dense(num_neuron_per_layer, activation=hidden_act_funct)

    if(is_l1):
        input_layer = Dense(num_neuron_per_layer, input_dim=len(df_train.columns)-1, activation=hidden_act_funct, kernel_regularizer=regularizers.l1(l1rate))
        hidden_layer = Dense(num_neuron_per_layer, activation=hidden_act_funct, kernel_regularizer=regularizers.l1(l1rate))

    elif(is_l2):
        input_layer = Dense(num_neuron_per_layer, input_dim=len(df_train.columns)-1, activation=hidden_act_funct, kernel_regularizer=regularizers.l2(l2rate))
        hidden_layer = Dense(num_neuron_per_layer, activation=hidden_act_funct, kernel_regularizer=regularizers.l2(l2rate))


    model = Sequential()
    model.add(input_layer)

    if(is_dropout):
        model.add(Dropout(0.25))

    for x in range(num_layers):
        model.add(hidden_layer)
        if (is_dropout):
            model.add(Dropout(droprate))

    model.add(Dense(num_possible_outcomes, activation=activationsl))

    model.compile(loss=lossl, optimizer=opt1, metrics=["mse"])

    model.fit(
        X_train,
        Y_train,
        epochs=100,
        batch_size= bch_sz,
        shuffle=True,
        verbose=2, #Change to 0 in final product --------------------------------------------------------------------
        validation_data=(X_test, Y_test)
    )

    test_accuracy = model.evaluate(X_test, Y_test)
    print("The error-rate for the test data set is: {}, ", test_accuracy)

    return model #'''
#-------------------------------End of Makeshift Fc----------------------------------------------------------------
#----------------------End of Models------------------------------------------------------------------

def row_correction(df):
    for index in range(len(df.index)):
        for column in range(len(df.columns)):
            if (isNaN(df.iloc[index].iloc[column])):
                df.iloc[index, column] = 0
            elif (np.isinf(df.iloc[index].iloc[column])):
                df.iloc[index, column] = 0
    return df

def make_l1_model(df):
    df_train = df[:2000]
    df_test = df[2000:]
    model = mk_fcnn(3, 100, 'relu', df_train, df_test, 185, 1,
            100, is_dropout = False, droprate = 0.5, is_l1 = True, l1rate = 0.01, is_l2 = False, l2rate = 0.01)#, categ_target = True)
    export_model(model, "l1NN")
    auc = calc_auroc(model, df_test)
    print("l1 auc score is: ", auc)
    return auc

def make_drop_model(df):
    df_train = df[:2000]
    df_test = df[2000:]
    model = mk_fcnn(3, 150, 'relu', df_train, df_test, 185, 1,
            200, is_dropout = True, droprate = 0.5, is_l1 = False, l1rate = 0.01, is_l2 = False, l2rate = 0.01, categ_target = False)

    export_model(model, "dropNN")
    auc = calc_auroc(model, df_test)
    print("drop auc score is: ", auc)
    return auc

def make_l2_model(df):
    df_train = df[:2000]
    df_test = df[2000:]
    model = mk_fcnn(3, 150, 'relu', df_train, df_test, 185, 1,
                    500, is_dropout=False, droprate=0.5, is_l1=False, l1rate=0.01, is_l2=True, l2rate=0.01)#'''
    col_names = df.columns.values
    calc_auroc(model, df_test)

    export_model(model, "l2NN")
    auc = calc_auroc(model, df_test)
    print("l2 auc score is: ", auc)
    return auc

def downsampling(df):
    print("extracting positive rows")
    final_df = pd.DataFrame(columns=df.columns.values, dtype=float)
    for index, row in df.iterrows():
        if row[185] == 1:
            print("index: ", index, " is 1")
            final_df = final_df.append(df.iloc[index], ignore_index=True)
    print(len(final_df.index))
    print(len(df.index))
    df = df.drop(df[df[185] == 1].index)
    print(len(df.index))
    df = df.sample(frac=0.07)
    df = df.append(final_df, ignore_index=True)
    df = df.sample(frac=1).reset_index(drop=True)
    print(len(df.index))
    return df

def export_model(model, model_name):
    model_builder = tf.saved_model.builder.SavedModelBuilder(model_name)

    inputs = {
        'input': tf.saved_model.utils.build_tensor_info(model.input)
    }
    outputs = {
        'is_dead': tf.saved_model.utils.build_tensor_info(model.output)
    }

    signature_def = tf.saved_model.signature_def_utils.build_signature_def(
        inputs=inputs,
        outputs=outputs,
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
    )

    model_builder.add_meta_graph_and_variables(
        K.get_session(),
        tags=[tf.saved_model.tag_constants.SERVING],
        signature_def_map={
            tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: signature_def
        }
    )

    model_builder.save()
    return


def main(): #purely for testing     #calculates the AUC score
    df = pd.read_csv("feature_data.csv")
    feature_scalar = preprocessing.MinMaxScaler()
    feature_scalar.fit(df)
    transformed_df = pd.DataFrame(feature_scalar.transform(df))
    joblib.dump(feature_scalar, "feature_scaler.save")
    average = tffe.mean(transformed_df[185])
    transformed_df = downsampling(transformed_df)
    l2_auc = make_l2_model(transformed_df)
    drop_auc = make_drop_model(transformed_df)
    l1_auc = make_l1_model(transformed_df)

    data = [[l1_auc, l2_auc, drop_auc]]
    auc_df = pd.DataFrame(data, columns=['l1_auc', 'l2_auc', 'drop_auc'])
    auc_df.to_csv("auc.csv", index=False)
    print(average)#'''



    '''
    df = pd.read_csv("feature_data.csv")
    feature_scalar = preprocessing.MinMaxScaler()
    feature_scalar.fit(df)
    joblib.dump(feature_scalar, "feature_scaler.save")#'''

    #'''
    #df = pd.read_csv("feature_data.csv")
    '''df = pd.read_csv("trashdb.csv")
    df = df.drop("Date", axis=1)
    df = df.drop("charttime", axis=1)
    scaler = preprocessing.MinMaxScaler()
    #prcol.fit(df["Val1"])
    scaler.fit(df)
    print(scaler.data_max_)
    joblib.dump(scaler, "scaler.save")#'''
    '''df = pd.read_csv("trashdb.csv")
    df = df.drop("Date", axis=1)
    df = df.drop("charttime", axis=1)
    scaler = joblib.load("scaler.save")
    transformed_df = scaler.transform(df)
    print(transformed_df[9])#'''
    return

#'''
if __name__=="__main__":
    main()
#'''
