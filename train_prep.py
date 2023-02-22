# split images into train, test, val
# create yaml file

from ultralytics import YOLO
import os
from os import path, mkdir
import shutil
from sklearn.model_selection import train_test_split
from IPython.display import display, Image
from IPython import display

# Utility function to copy files
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.copy(f, destination_folder)
        except:
            print(f)
            assert False

# create yaml file
def create_yaml():
    content = '''train: ../data_split/images/train/
val: ../data_split/images/val/
test: ../data_split/images/test/

nc: 1

names: ["mushroom"]'''

    f = open("./yolov5/data/mushroom.yaml", "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
    # Read images and annotations
    images = [os.path.join('./created_images/images', x) for x in os.listdir('./created_images/images')]
    annotations = [os.path.join('./created_images/labels', x) for x in os.listdir('./created_images/labels') if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits (0.8, 0.1, 0.1 ratio)
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

    # create folders to keep splits
    splits = "./data_split"
    if not path.exists(splits):
        mkdir(splits)
    if not path.exists(splits + "/images"):
        mkdir(splits + "/images")
    if not path.exists(splits + "/labels"):
        mkdir(splits + "/labels")

    if not path.exists(splits + "/images/train"):
        mkdir(splits + "/images/train")
    if not path.exists(splits + "/images/test"):
        mkdir(splits + "/images/test")
    if not path.exists(splits + "/images/val"):
        mkdir(splits + "/images/val")
    if not path.exists(splits + "/labels/train"):
        mkdir(splits + "/labels/train")
    if not path.exists(splits + "/labels/test"):
        mkdir(splits + "/labels/test")
    if not path.exists(splits + "/labels/val"):
        mkdir(splits + "/labels/val")


    # Move the splits into their folders
    move_files_to_folder(train_images, splits + '/images/train')
    move_files_to_folder(val_images, splits + '/images/val')
    move_files_to_folder(test_images, splits + '/images/test')
    move_files_to_folder(train_annotations, splits + '/labels/train')
    move_files_to_folder(val_annotations, splits + '/labels/val')
    move_files_to_folder(test_annotations, splits + '/labels/test')

    create_yaml()

    # RUN :
    # python ./yolov5/train.py  --batch 32 --epochs 1000 --data mushroom.yaml --weights yolov5s.pt --device 0

    # to check:
    # python ./yolov5/detect.py --weights yolov5/runs/train/exp6/weights/best.pt  --conf 0.4 --source ./data_split/images/train/1-1_0.jpg