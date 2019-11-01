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

