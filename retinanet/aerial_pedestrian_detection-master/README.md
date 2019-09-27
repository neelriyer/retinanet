# Keras RetinaNet on Stanford Drone Data Set [![Build Status](https://travis-ci.org/fizyr/keras-retinanet.svg?branch=master)](https://travis-ci.org/fizyr/keras-retinanet) [![DOI](https://zenodo.org/badge/100249425.svg)](https://zenodo.org/badge/latestdoi/100249425)

Keras implementation of RetinaNet object detection as described in [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002)
by Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He and Piotr Dollár.

This code is borrowed from Keras Implementation of this model at https://github.com/fizyr/keras-retinanet and updated to run on Stanford Drone Data Set

## Installation

1) Clone this repository.
2) Ensure numpy is installed using `pip install numpy --user`
3) In the repository, execute `pip install . --user`.
   Note that due to inconsistencies with how `tensorflow` should be installed,
   this package does not define a dependency on `tensorflow` as it will try to install that (which at least on Arch Linux results in an incorrect installation).
   Please make sure `tensorflow` is installed as per your systems requirements.
4) Alternatively, you can run the code directly from the cloned  repository, however you need to run `python setup.py build_ext --inplace` to compile Cython code first.
5) Optionally, install `pycocotools` if you want to train / test on the MS COCO dataset by running `pip install --user git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI`.


## Training on custom data set (added by Priyanka Dwivedi)
For training on a [custom dataset], a CSV file can be used as a way to pass the data.
See below for more details on the format of these CSV files.


To train using your CSV, run:
### Running directly from the repository:
```
keras_retinanet/bin/train.py --weights snapshots/resnet50_coco_best_v2.1.0.h5 csv train_annotations.csv labels.csv --val-annotations val_annotations.csv
```

Here 
* weights: Path to the weights for initializing training
* csv indicates retinanet is trained on a custom data set
* train_annotations.csv is path to training annotations
* labels.csv are the labels in the format class_name, class_id with 0 reserved for background class
* val_annotations is path to validation annotations 

### Training Images
I uploaded the images used for training and validation to the google drive link below. Please download the same:
https://drive.google.com/drive/u/0/folders/1bLt6KK_9zKogJdvW-lKh9BnBKgFfvPp9

### Annotations format
The CSV file with annotations should contain one annotation per line.
Images with multiple bounding boxes should use one row per bounding box.
Note that indexing for pixel values starts at 0.
The expected format of each line is:
```
path/to/image.jpg,x1,y1,x2,y2,class_name
```

### Labels format
The class name to ID mapping file should contain one mapping per line.
Each line should use the following format:
```
class_name,id
```

For the Stanford Drone Data Set, the training annotations are in train_annotations.csv, validation annotations are in val_annoations.csv and labels are in labels.csv


## Evaluating Results (added by Priyanka Dwivedi)

To calculate mean average precision on the validation set, please run

```
keras_retinanet/bin/evaluate.py csv val_annotations.csv labels.csv snapshots/resnet50_csv_08_inference.h5 --convert-model
```

Here we pass the val_annotations, labels and path to the trained weights


## Running Inference on Images and Videos (added by Priyanka Dwivedi)

To run inference on the trained model, first step is to convert the trained model to a format that can be used by inference. The command for this is:

```
keras_retinanet/bin/convert_model.py snapshots/resnet50_csv_08.h5 snapshots/resnet50_csv_08_inference.h5 
```

Here first path is the path to the trained model and the second would be the path to the converted inference model

I created two notebooks from the original code that can be used to run inference on images and on videos.

The notebooks are:
* ResNet50RetinaNet-Image.ipynb : For inference on a batch of images
* ResNet50RetinaNet-Video.ipynb : For inference on a video

I ran inference on one of the videos from Stanford Drone Data Set and shared here as death_circle_output.mp4.

## Error Analysis (add by Priyanka Dwivedi)
The notebook ResNet50RetinaNet-Error-Analysis.ipynb can be used for error analysis and can help visualize true positive, class mismatch, false positive and false negative predictions

