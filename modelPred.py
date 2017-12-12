import pandas as pd
import numpy as np
import os
import pickle
import gc
import xgboost as xgb
import numpy as np
import re
import pandas as pd
from sklearn.model_selection import train_test_split

labels=['PLAIN', 'PUNCT', 'DATE', 'LETTERS', 'CARDINAL', 'VERBATIM', 'DECIMAL','MEASURE', 'MONEY', 'ORDINAL', 'TIME', 'ELECTRONIC', 'DIGIT','FRACTION', 'TELEPHONE', 'ADDRESS']
num_class=len(labels)
max_num_features = 10
pad_size = 1
boundary_letter = -1
space_letter = 0
max_data_size = 960000
max_data_size = 40

out_path = r'.'
df = pd.read_csv(r'C:\Users\sxzho\Desktop\kaggle\test\en_test_2.csv')


x_data = []
num_class = len(labels)

for x in df['before'].values:
    x_row = np.ones(max_num_features, dtype=int) * space_letter
    for xi, i in zip(list(str(x)), np.arange(max_num_features)):
        x_row[i] = ord(xi)
    x_data.append(x_row)

def context_window_transform(data, pad_size):
    pre = np.zeros(max_num_features)
    pre = [pre for x in np.arange(pad_size)]
    data = pre + data + pre
    neo_data = []
    for i in np.arange(len(data) - pad_size * 2):
        row = []
        for x in data[i : i + pad_size * 2 + 1]:
            row.append([boundary_letter])
            row.append(x)
        row.append([boundary_letter])
        neo_data.append([int(x) for y in row for x in y])
    return neo_data

x_data = np.array(context_window_transform(x_data, pad_size))
gc.collect()
x_data = np.array(x_data)

ddata = xgb.DMatrix(x_data)

param = {'objective':'multi:softmax',
         'eta':'0.3', 'max_depth':10,
         'silent':1, 'nthread':-1,
         'num_class':num_class,
         'eval_metric':'merror'}
gc.collect()


bst = xgb.Booster({'nthread': 4})  # init model
bst.load_model(os.path.join(out_path, 'xgb_model'))  # load data

pred = bst.predict(ddata)
pred=list(map(int,pred))
df.assign(label2=pred)
df["label"]=pred
#pred = [labels[int(x)] for x in pred]
import csv
df.to_csv("label.csv",index=False,quoting=csv.QUOTE_NONNUMERIC)
'''
y_valid = [labels[x] for x in y_valid]
x_valid = [ [ chr(x) for x in y[2 + max_num_features: 2 + max_num_features * 2]] for y in x_valid]
x_valid = [''.join(x) for x in x_valid]
x_valid = [re.sub('a+$', '', x) for x in x_valid]

gc.collect()

df_pred = pd.DataFrame(columns=['data', 'predict', 'target'])
df_pred['data'] = x_valid
df_pred['predict'] = pred
df_pred['target'] = y_valid
df_pred.to_csv(os.path.join(out_path, 'pred.csv'))

df_erros = df_pred.loc[df_pred['predict'] != df_pred['target']]
df_erros.to_csv(os.path.join(out_path, 'errors.csv'), index=False)
'''
