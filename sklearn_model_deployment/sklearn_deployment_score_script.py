

########################################################################################################
#
#   Sklearn Scoring
#
########################################################################################################

import os,sys,csv,re
import time,datetime
import pandas as pd
import numpy as np
import scipy as sp
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
from sklearn.metrics import explained_variance_score, r2_score, mean_squared_error

########################################################################################################
#
#   Global Functions - Used for both Model Building and Model Scoring
#
########################################################################################################


def define_schema():
    dtypes    = {
                    'age':np.int64, 
                    'workclass':np.object, 
                    'fnlwgt':np.int64, 
                    'education':np.object, 
                    'education_num':np.int64, 
                    'martial_status':np.object, 
                    'occupation':np.object, 
                    'relationship':np.object, 
                    'race':np.object, 
                    'sex':np.object, 
                    'capital_gain':np.int64, 
                    'capital_loss':np.int64, 
                    'hours_per_week':np.int64, 
                    'native_country':np.object
                }
    col_names = [k for k,v in dtypes.iteritems()]
    return dtypes, col_names


def variables_to_ignore_in_model():
    return ['income']


def get_list_of_numerics_vars(df):
    vars_ignore = variables_to_ignore_in_model()
    return [col[0] for col in df.dtypes.iteritems() if (col[1].name in ['int64','uint64','float64']) and (col[0] not in vars_ignore)]


def get_list_of_categorical_vars(df):
    vars_ignore = variables_to_ignore_in_model()
    return [col[0] for col in df.dtypes.iteritems() if (col[1].name in ['object']) and (col[0] not in vars_ignore)]


def transform_get_dummies(df):
    categorical_vars = get_list_of_categorical_vars(df)
    return pd.get_dummies(df, columns=categorical_vars)


def transform_drop_ignored_vars(df):
    vars_ignore = variables_to_ignore_in_model()
    if any(i in df.columns.tolist() for i in vars_ignore):
        return df.drop( vars_ignore, axis=1, inplace=True)
    else:
        return df


def transform_fillna(df):
    return df.fillna(-1)

########################################################################################################
#
#   Input Data
#
########################################################################################################

dtypes, col_names = define_schema()

try:
    df_filepath = sys.argv[1]
    df = pd.read_table(df_filepath, sep=",", header=None, names=col_names)
except:
    print '[ ERROR ] Either your filepath is incorrect or the data is not suitable for this model. Make sure that your data contains the following inputs:\n'
    for i,col in enumerate(col_names):
        print '\t' + str(i) + '\t' + str(col)


########################################################################################################
#
#   Transformations
#
########################################################################################################

transformed_df = transform_get_dummies(df)
transformed_df = transform_drop_ignored_vars(transformed_df)
transformed_df = transform_fillna(transformed_df)

########################################################################################################
#
#   Score Model
#
########################################################################################################

dt_saved = pickle.load(open('/tmp/dt.sav', 'rb'))
predicted = dt_saved.predict(transformed_df)

# Append "predicted scores" to original DF.
df['predicted'] = pd.DataFrame(predicted)

# Save to Database, filesystem, Hadoop, etc. 
df.to_csv('/tmp/my_scored_data.csv')


#ZEND