from PIL import Image
from os import path, mkdir
import random
import json
import pandas as pd

# resize image (shrink) by a scale factor s
def shrink(img, s):
    size = (int(img.size[0] / s), int(img.size[1] / s))
    return img.resize(size)

# overlay img2 onto img1
def place_image(img1, img2, c, flip=False):   
    if flip:    # randomly flip image
        flip = random.randint(0, 1)
        if flip:
            img2 = img2.transpose(method=Image.FLIP_LEFT_RIGHT)
            
    # Pasting img2 image on top of copy of img1
    img = img1.copy()
    img.paste(img2, c, mask = img2)
    return img

# create n images by merging img1 and img 2 and save to designated directory
# also create dataframe and save info
'''
dataframe columns:
filename: filename of generated image. format of number + .jpg
class: if image contains mushroom or not. generated images all contain mushrooms, default value is True
width: width of generated image
height: height of generated image
xmin, ymin, xmax, ymax: coordinates for bounding box
'''
def create_save_images(n, mushroom, background, scale, start_coord, flip, path):
    df = pd.DataFrame(columns = ["filename", "class", "width", "height", 'xmin', 'ymin', 'xmax', 'ymax'])

    # Opening background image (used in background)
    img1 = Image.open("./nature images/" + str(background) + ".jpg")
    
    # Opening mushroom image (overlay image)
    img2 = Image.open("./mushroom images/" + str(mushroom) + ".png")

    max_coord = (img1.size[0]-img2.size[0], img1.size[1]-img2.size[1])

    # create and save image
    for i in range(n):
        # random range of coordinates c1 ~ c2
        random_coord = (random.randint(start_coord[0], max_coord[0]), random.randint(start_coord[1], max_coord[1]))

        # scale image by y coordinate
        # print(img2.size)
        obj = shrink(img2, scale[0] * (img1.size[1] / random_coord[1]) ** scale[1])
        # print(obj.size)

        # place img2 (obj) onto img1
        img = place_image(img1, obj, random_coord, flip)
        filename = str(mushroom) + '-' + str(background) + "_" + str(i) + '.jpg'
        img.save(path + '/' + filename)

        # create and save dataframe
        data = [filename, "mushroom", img.size[0], img.size[1], random_coord[0], random_coord[1], random_coord[0] + obj.size[0], random_coord[1] + obj.size[1]]
        s = pd.Series(data, index=df.columns)
        df = df.append(s, ignore_index=True)
        df.to_csv(path + '/data.csv', index=False)

# helper functions for creating coco dataset
def image(row):
    image = {}
    image["height"] = row.height
    image["width"] = row.width
    image["id"] = row.fileid
    image["file_name"] = row.filename
    return image
def _category(row):
    category = {}
    category["supercategory"] = 'None'
    category["id"] = row.categoryid
    category["name"] = row[2]
    return category
def annotation(row):
    annotation = {}
    area = (row.xmax -row.xmin)*(row.ymax - row.ymin)
    annotation["segmentation"] = []
    annotation["iscrowd"] = 0
    annotation["area"] = area
    annotation["image_id"] = row.fileid
    annotation["bbox"] = [row.xmin, row.ymin, row.xmax -row.xmin,row.ymax-row.ymin ]
    annotation["category_id"] = row.categoryid
    annotation["id"] = row.annid
    return annotation        

# create coco dataset from csv file with above format
def csv_to_coco(filename, output_folder):
    data = pd.read_csv(filename)
    images = []
    categories = []
    annotations = []

    category = {}
    category["supercategory"] = 'none'
    category["id"] = 0
    category["name"] = 'None'
    categories.append(category)

    data['fileid'] = data['filename'].astype('category').cat.codes
    data['categoryid']= pd.Categorical(data['class'],ordered= True).codes
    data['categoryid'] = data['categoryid']+1
    data['annid'] = data.index
    for row in data.itertuples():
        annotations.append(annotation(row))

    imagedf = data.drop_duplicates(subset=['fileid']).sort_values(by='fileid')
    for row in imagedf.itertuples():
        images.append(image(row))

    catdf = data.drop_duplicates(subset=['categoryid']).sort_values(by='categoryid')
    for row in catdf.itertuples():
        categories.append(_category(row))

    data_coco = {}
    data_coco["images"] = images
    data_coco["categories"] = categories
    data_coco["annotations"] = annotations
    json.dump(data_coco, open(output_folder + "/cocodata.json", "w"), indent=4)



# if __name__ == "__main__":

#     # Opening the primary image (used in background)
#     img1 = Image.open("./nature images/2.jpg")
    
#     # Opening the secondary image (overlay image)
#     img2 = Image.open("./mushroom images/3.png")

#     # scale format: (shrink factor, (image size / mushroom y coord))
#     scale = (1.5, 2)

#     start_coord = (0, 456)
#     max_coord = (img1.size[0]-img2.size[0], img1.size[1]-img2.size[1])

#     output_folder = "./created_images"
#     if not path.exists(output_folder):
#         mkdir(output_folder)

#     create_save_images(100, img1, img2, scale, start_coord, max_coord, True, output_folder)
#     csv_to_coco(output_folder + "/data.csv", output_folder)

#     # img = random_place_image(img1, img2, start_coord, max_coord)
#     # img.show()
