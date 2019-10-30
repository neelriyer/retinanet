#!/bin/sh

echo "building csv: supervisely_to_csv.py"
python supervisely_to_csv.py

echo "adding spacenet data"
python tf_to_retinanet.py

echo "building training and test csv"
python training_test_split.py

echo "making changes to new data"
python spacenet_train_test_split.py
python delete_row.py

echo "changing directory"
cd aerial_pedestrian_detection-master

echo "pip install"
pip install . --user

echo "setup.py"
python setup.py build_ext --inplace

echo "beginning training"
python keras_retinanet/bin/train.py  --config config.ini csv train_annotations_new_data.csv labels_new_data.csv

