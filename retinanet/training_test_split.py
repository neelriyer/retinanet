#train test split

#script to split csv file into train test

import pandas as pd
import numpy as np
import os

path = os.getcwd()
df = pd.read_csv(path+'/processed_JSON/retinanet_data.csv')


#df['split'] = np.random.randn(df.shape[0], 1)

#msk = np.random.rand(len(df)) <= 0.7

#train = df[msk]
#test = df[~msk]

train, validate, test = np.split(df.sample(frac=1), [int(.6*len(df)), int(.8*len(df))])


if os.path.exists(os.getcwd()+'/train_annotations.csv'):
	os.remove(os.getcwd()+'/train_annotations.csv')

if os.path.exists(os.getcwd()+'/test_annotations.csv'):
	os.remove(os.getcwd()+'/test_annotations.csv')

if os.path.exists(os.getcwd()+'/val_annotations.csv'):
	os.remove(os.getcwd()+'/val_annotations.csv')


train.to_csv(os.getcwd()+'/train_annotations.csv', header=True, index=None, sep=',', mode='a')
test.to_csv(os.getcwd()+'/test_annotations.csv', header=True, index=None, sep=',', mode='a')
validate.to_csv(os.getcwd()+'/val_annotations.csv', header=True, index=None, sep=',', mode='a')



