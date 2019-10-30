#spacenet train test split

import pandas as pd 
import os
import numpy as np

#read csv
df = pd.read_csv(os.getcwd()+'/processed_JSON/retinanet_data_spacenet.csv')
train_existing = pd.read_csv(os.getcwd()+'/train_annotations.csv')
test_existing = pd.read_csv(os.getcwd()+'/test_annotations.csv')


def train_test_split(new_df, split):

	msk = np.random.rand(len(new_df)) < split
	train = new_df[msk]
	test = new_df[~msk]


	return train, test

#function to get picture name
def get_image_name(df):

	df['image'] = None
	for index, row in df.iterrows():

		#get image
		df['image'][index] = str(df['path'][index].split('/')[-1].split('.')[0])

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

# get picture name
df = get_image_name(df)
print(df.head())

new_df = create_new_unqiue_df(df)
print(new_df)

train, test = train_test_split(new_df, 0.9)
print(len(train))
print(len(test))
print(len(new_df))

#TRAINGIN SET

print('training set')
print(train.head())

#inner join with df
training_df = pd.merge(left=train,right=df, left_on='image', right_on='image')


print('\n\ntraining set')
print(training_df[['image', 'class_title']].head(10))



#TESTING SET
#left join with df
print('\n\ntesting set')
print(test.head())

#inner join with df
testing_df = pd.merge(left=test,right=df, left_on='image', right_on='image')


print('\n\ntest set')
print(testing_df[['image','class_title']].head(10))

#check
if(len(testing_df)+len(training_df)==len(df)):
	print("train test completed successfully")
else:
	raise "error occured"


#NOW APPEND NEW DATA TO OLD DATA
train_to_append = training_df.drop('image', axis = 1)
test_to_append = testing_df.drop('image', axis = 1)


#append
train = train_existing.append(train_to_append)
test = test_existing.append(test_to_append)

print('after append')
print(train['path'].apply(lambda text: text.split('/')[-1]))
print(test['path'].apply(lambda text: text.split('/')[-1]))



#remove files if they exist
if os.path.exists(os.getcwd()+'/train_annotations_spacenet.csv'):
	os.remove(os.getcwd()+'/train_annotations_spacenet.csv')

if os.path.exists(os.getcwd()+'/test_annotations_spacenet.csv'):
	os.remove(os.getcwd()+'/test_annotations_spacenet.csv')

#to csv
train.to_csv(os.getcwd()+'/train_annotations_spacenet.csv', header=True, index=None, sep=',', mode='a')
test.to_csv(os.getcwd()+'/test_annotations_spacenet.csv', header=True, index=None, sep=',', mode='a')


