#delete first row of csv file

with open("train_annotations.csv",'r') as f:
    with open("aerial_pedestrian_detection-master/train_annotations_new_data.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

with open("test_annotations.csv",'r') as f:
    with open("aerial_pedestrian_detection-master/test_annotations_new_data.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

with open("val_annotations.csv",'r') as f:
    with open("aerial_pedestrian_detection-master/val_annotations_new_data.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)