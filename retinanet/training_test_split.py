#train test split

#script to split csv file into train test

import pandas as pd
import numpy as np
import os

#read csv
df = pd.read_csv(os.getcwd()+'/processed_JSON/retinanet_data.csv')


#function to get x and y coordinates from image path
def get_x_y_coords(df):

	df['image'] = None
	df['x'] = None
	df['y'] = None
	for index, row in df.iterrows():

		#get image
		df['image'][index] = str(df['path'][index].split('/')[-1])

		#get x and y coordinates
		df['x'][index] = int(df['path'][index].split('/')[-1].split('_')[0].split('.')[0])
		df['y'][index] = int(df['path'][index].split('/')[-1].split('_')[-1].split('.')[0])

	return df

#function to create new unique dataframe that drops duplicates
def create_new_unqiue_df(df):

	#create new dataframe of only image
	new_df = pd.DataFrame()
	new_df['image'] = df['image'].astype(str)

	#drop duplicates from new_df
	new_df = new_df.drop_duplicates(subset=['image'], keep='first') 

	#reindex dataframe
	new_df.index = [x for x in range(len(new_df))]


	return new_df

#create train and test
#split into train and test
def train_test_split(new_df):

	msk = np.random.rand(len(new_df)) < 0.8
	train = new_df[msk]
	test = new_df[~msk]


	return train, test

#get x and y coordinates from image
df = get_x_y_coords(df)
df = df.sort_values(by=['x', 'y'])
print(df[['image', 'x', 'y', 'class_title']].head(10))

#create new df with image, x and y cols and drop duplicate columns in iamges
new_df = create_new_unqiue_df(df)


#split into training and test
train, test = train_test_split(new_df)


#TRAINGIN SET

print('training set')
print(train.head())

#inner join with df
training_df = pd.merge(left=train,right=df, left_on='image', right_on='image')

#sort values
training_df = training_df.sort_values(by=['x', 'y'])
print('\n\ntraining set')
print(training_df[['image', 'x', 'y', 'class_title']].head(10))


#TESTING SET
#left join with df
print('\n\ntesting set')
print(test.head())

#inner join with df
testing_df = pd.merge(left=test,right=df, left_on='image', right_on='image')

#sort values
testing_df = testing_df.sort_values(by=['x', 'y'])

print('\n\ntest set')
print(testing_df[['image', 'x', 'y', 'class_title']].head(10))

#check
if(len(testing_df)+len(training_df)==len(df)):
	print("train test completed successfully")
else:
	raise "error occured"



#remove files if they exist
if os.path.exists(os.getcwd()+'/train_annotations.csv'):
	os.remove(os.getcwd()+'/train_annotations.csv')

if os.path.exists(os.getcwd()+'/test_annotations.csv'):
	os.remove(os.getcwd()+'/test_annotations.csv')


#drop cols created for this script
training_df = training_df.drop(['image', 'x', 'y'], axis = 1)
testing_df = testing_df.drop(['image', 'x', 'y'], axis = 1)

#length
print(len(testing_df))
print(len(training_df))

#write to csv
testing_df.to_csv(os.getcwd()+'/train_annotations.csv', header=True, index=None, sep=',', mode='a')
training_df.to_csv(os.getcwd()+'/test_annotations.csv', header=True, index=None, sep=',', mode='a')



