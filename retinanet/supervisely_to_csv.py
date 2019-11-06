
#supervisely_to_csv.py
#read data from superisely images and convert to csv file for retinanet model

import cv2
import os
import json
import pandas as pd
import math
import shutil

#GLOBALS
Dataset = 'processed_JSON'

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



#get context around each driveway
def context_creator(x_start, y_start, x_finish, y_finish, path_to_img):

	#get size of image
	img = cv2.imread(path_to_img,0)
	height, width = img.shape[:2]

	#find long side
	x_distance = abs(x_finish-x_start)
	y_distance = abs(y_finish-y_start)

	#if longer in x than y
	if(x_distance > y_distance):

		#elongate in y
		if(y_start - 10>=0):
			y_start = y_start - 10

		if(y_finish + 10<=height):
			y_finish = y_finish + 10

		#slightly elongate in x
		if(x_start - 3>=0):
			x_start = x_start - 3

		if(x_finish + 3 <=width):
			x_finish = x_finish + 3

	#if longer in y than x
	if(y_distance > x_distance):

		#elongate in x
		if(x_start - 10>=0):
			x_start = x_start - 10

		if(x_finish + 10 <=width):
			x_finish = x_finish + 10

		#slighly elongate in y
		if(y_start - 3>=0):
			y_start = y_start - 3

		if(y_finish + 3<=height):
			y_finish = y_finish + 3


	return x_start, y_start, x_finish, y_finish



#function to return max width and height of bounding box
#creates an all encompasing bounding box
def bbox(points):

	#list of coordiantes
	x_coord = []
	y_coord = []

	for pt in points:

		#append x and y coordinates
		x_coord.append(int(pt[0]))
		y_coord.append(int(pt[1]))

	#initialise starts and finishes
	x_start, y_start, x_finish, y_finish = min(x_coord), min(y_coord), max(x_coord), max(y_coord)

	if(x_start == x_finish):
		x_finish = x_finish + 1
	if(y_start == y_finish):
		y_finish = y_finish + 1

	return x_start, y_start, x_finish, y_finish

	

#function to take json file from path and convert the information inside to a pandas dataframe
def JSON_to_dataframe(path, folder_name):

	with open(path, 'r') as f:

		data_dict = json.load(f)
		objects_list = data_dict['objects']
		#print(len(objects_list))

		#print(objects_list)

		#create dataframe
		df = pd.DataFrame()

		#get coordinates into dataframe
		for i in range(len(objects_list)):

			#get location of iamge
			location = path.split('/')[-1].split('.')[0]
			path_to_img = os.getcwd() + '/labelled_images/' + folder_name + '/img/' + location + '.jpg'
			print(path_to_img)

			#read coordinates from JSON
			points = objects_list[i]['points']['exterior']

			#parkinglot found
			if(objects_list[i]['classTitle']=='Poly'):
				print('parkinglot detected')
				print(points)

				#get bounding box for parkignlot
				x_start, y_start, x_finish, y_finish = bbox(points)

				#print out x_start, y_start, x_finish, y_finish
				print('x_start is ' + str(x_start))
				print('y_start is ' + str(y_start))
				print('x_finish is ' + str(x_finish))
				print('y_finish is ' + str(y_finish))
				print('\n\n')

				#append to dataframe
				df2 = {'path': path_to_img, 'x_start': x_start, 'y_start': y_start, 'x_finish': x_finish, 'y_finish': y_finish, 'class_title': 'parking lot'}
				df = df.append(df2, ignore_index = True)


			#driveway found
			elif(objects_list[i]['classTitle']=='driveways_line'):
				print('driveway detected')
				print(points)

				# get x and y starts and finishes
				x_start, y_start, x_finish, y_finish = bbox(points)


				#CHANGE THIS ONE LINE LATER IF NEED BE
				#INCREASES SIZE OF DRIVEWAYS
				x_start, y_start, x_finish, y_finish = context_creator(x_start, y_start, x_finish, y_finish, path_to_img) 

				#print out x_start, y_start, x_finish, y_finish
				print('x_start is ' + str(x_start))
				print('y_start is ' + str(y_start))
				print('x_finish is ' + str(x_finish))
				print('y_finish is ' + str(y_finish))
				print('\n\n')

				#append to dataframe
				df2 = {'path': path_to_img, 'x_start': x_start, 'y_start': y_start, 'x_finish': x_finish, 'y_finish': y_finish, 'class_title': 'driveway'}
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
create_directory(Dataset)

#return list of all folders in directory
def list_of_all_folders(directory):

	return next(os.walk(directory))[1]



x_files = list_of_all_folders(os.getcwd()+'/labelled_images/')
print(x_files)


df = pd.DataFrame()

#for each x_file
for x in x_files:

	#get all requires files in this folder
	files = list_of_files(os.getcwd()+'/labelled_images/'+str(x)+'/ann/')

	for file in files:

		#print(file)

		location = file.split('.', 2)[0]
		#print(location)

		path = os.getcwd()+'/labelled_images/'+str(x)+'/ann/' + file
		#print(path)

		new_df = JSON_to_dataframe(path, x)


		df = df.append(new_df, ignore_index = True)



#convert str to int
if(df is not None):

	df['x_start'] = df['x_start'].apply(lambda row: int(row))
	df['y_start'] = df['y_start'].apply(lambda row: int(row))
	df['x_finish'] = df['x_finish'].apply(lambda row: int(row))
	df['y_finish'] = df['y_finish'].apply(lambda row: int(row))
	#print(df)

	df.to_csv(os.getcwd()+'/'+Dataset+'/'+'retinanet_data_supervisely'+'.csv', header=True, index=None, sep=',', mode='a')


