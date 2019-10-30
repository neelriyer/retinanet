#spacenet train test split

import pandas as pd 
import os
import numpy as np

#read csv
df = pd.read_csv(os.getcwd()+'/processed_JSON/retinanet_data_spacenet.csv')
train_existing = pd.read_csv(os.getcwd()+'/train_annotations.csv')
test_existing = pd.read_csv(os.getcwd()+'/test_annotations.csv')


def train_test_split(new_df):

	msk = np.random.rand(len(new_df)) < 0.8
	train = new_df[msk]
	test = new_df[~msk]


	return train, test

def convert_cols_to_int(df):
	df['x_start'] = df['x_start'].apply(lambda row: int(row))
	df['y_start'] = df['y_start'].apply(lambda row: int(row))
	df['x_finish'] = df['x_finish'].apply(lambda row: int(row))
	df['y_finish'] = df['y_finish'].apply(lambda row: int(row))

	return df

#split
train_to_append, test_to_append = train_test_split(df)

print(train_to_append.head())
print(test_to_append.head())

print(train_existing.head())
print(test_existing.head())


#append
train = train_existing.append(train_to_append)
test = test_existing.append(test_to_append)

print('after append')
print(train.head())
print(test.head())




#remove files if they exist
if os.path.exists(os.getcwd()+'/train_annotations_spacenet.csv'):
	os.remove(os.getcwd()+'/train_annotations_spacenet.csv')

if os.path.exists(os.getcwd()+'/test_annotations_spacenet.csv'):
	os.remove(os.getcwd()+'/test_annotations_spacenet.csv')

#to csv
test.to_csv(os.getcwd()+'/train_annotations_spacenet.csv', header=True, index=None, sep=',', mode='a')
train.to_csv(os.getcwd()+'/test_annotations_spacenet.csv', header=True, index=None, sep=',', mode='a')




