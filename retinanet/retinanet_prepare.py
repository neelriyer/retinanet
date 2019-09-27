#script to prepare data for retinanet
#analyses labelled images (in labelled images folder)
#converts JSON to required information

"""
will extract:

- classification of image
- x1 pixel coordinate of driveway/curb/offstreet parking bay
- x2 pixel coordinate of driveway/curb/offstreet parking bay
- y1 pixel coordinate of driveway/curb/offstreet parking bay
- y2 pixel coordinate of driveway/curb/offstreet parking bay
- path to image

keras_retinanet/bin/convert_model.py snapshots/resnet50_coco_best_v2.1.0.h5 snapshots/resnet50_coco_best_v2.1.0_inference.h5 


"""

import os
import json
import pandas as pd
import math
import shutil

#function to get list of files in directory
def list_of_files(mypath):
	from os import listdir
	from os.path import isfile, join
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	return files

#use pythogas's theorem to calculate distance between coorindates
def calculate_distance(x1,y1,x2,y2):  
	 dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
	 return dist  

#function to calculate midpoint of two points
def calculate_midpoint(x1,y1,x2,y2):
	return ((x1+x2)/2, (y1+y2)/2)

#function to do division that avoids division by zero
def calculate_angle(y_distance, x_distance):

	#if divide by zero angle is vertical so 90 degrees
	try:
		angle = math.degrees(math.atan(y_distance/x_distance))

	except:
		angle = 90

	return angle
	

#function to take json file from path and convert the information inside to a pandas dataframe
def JSON_to_dataframe(path):

	with open(path, 'r') as f:

		data_dict = json.load(f)
		objects_list = data_dict['objects']
		#print(len(objects_list))

		#print(objects_list)

		#create dataframe
		df = pd.DataFrame()

		#get coordinates into dataframe
		for i in range(len(objects_list)):

			location = path.split('/')[-1].split('.')[0]
			folder_name = location.split('_')[0]
			path_to_img = os.getcwd() + '/labelled_images/' + folder_name + '/img/' + location + '.jpg'
			print(path_to_img)

			#start and finish coordinates of each line
			start = objects_list[i]['points']['exterior'][0]
			finish = objects_list[i]['points']['exterior'][1]

			#get x and y coordiantes
			#starts
			x_start = start[0] 
			y_start = start[1] 

			#finish
			x_finish = finish[0] 
			y_finish = finish[1] 

			#if x_start is greater than x_finish swap x_start and x_finish
			if(x_start>x_finish):
				temp = x_start
				x_start = x_finish
				x_finish = temp
				#print('swapped')

			#if y_start is greater than y_finish swap y_start and y_finish
			if(y_start>y_finish):
				temp = y_start
				y_start = y_finish
				y_finish = temp
				#print('swapped')

			#if x_start is equal to x_finish increment x_finish by 1
			if(x_start==x_finish):
				x_finish = x_finish + 1

			#if y_start is equal to y_finish increment y_finish by 1
			if(y_start==y_finish):
				y_finish = y_finish + 1
				

			print('x_start is ' + str(x_start))
			print('x_finish is ' + str(x_finish))

			print('y_start is ' + str(y_start))
			print('y_finish is ' + str(y_finish))
			print('\n\n')

			df2 = {'path': path_to_img, 'x_start': x_start, 'y_start': y_start, 'x_finish': x_finish, 'y_finish': y_finish, 'class_title': objects_list[i]['classTitle']}
			df = df.append(df2, ignore_index = True)

		try:
			final_df = df[['path', 'x_start', 'y_start', 'x_finish', 'y_finish', 'class_title']]
			return final_df

		except:
			return None

#function to create directory
#replace directory is if already exists
def create_directory(directory_name):
	name = os.getcwd()+'/'+str(directory_name)
	try:
		os.makedirs(name)    
	except FileExistsError:
		shutil.rmtree(name) 
		os.makedirs(name)  


#create new directory
create_directory('processed_JSON')


x_files = ['1855744','1855745','1855746', '1855747']

df = pd.DataFrame()

for x in x_files:

	#get all requires files in this folder
	files = list_of_files(os.getcwd()+'/labelled_images/'+str(x)+'/ann/')

	for file in files:

		#print(file)

		location = file.split('.', 2)[0]
		#print(location)

		path = os.getcwd()+'/labelled_images/'+str(x)+'/ann/' + file
		#print(path)

		df = df.append(JSON_to_dataframe(path), ignore_index = True)



#convert str to int
if(df is not None):

	df['x_start'] = df['x_start'].apply(lambda row: int(row))
	df['y_start'] = df['y_start'].apply(lambda row: int(row))
	df['x_finish'] = df['x_finish'].apply(lambda row: int(row))
	df['y_finish'] = df['y_finish'].apply(lambda row: int(row))
	#print(df)

	df.to_csv(os.getcwd()+'/processed_JSON/'+'retinanet_data'+'.csv', header=True, index=None, sep=',', mode='a')


