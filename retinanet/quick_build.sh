#!/bin/sh

echo "changing directory"
cd aerial_pedestrian_detection-master

echo "pip install"
pip install . --user

echo "setup.py"
python setup.py build_ext --inplace

cd /

