from PIL import Image
from os import path, mkdir
import random
import json
import pandas as pd
import re

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
def mush_on_bg(n, mushroom, background, scale, start_coord, flip, path):
    df = pd.DataFrame(columns = ["filename", "class", "width", "height", 'xmin', 'ymin', 'xmax', 'ymax'])

    # Opening background image (used in background)
    img1 = Image.open("./nature images/" + str(background) + ".jpg")
    
    # Opening mushroom image (overlay image)
    img2 = Image.open("./mushroom images/" + str(mushroom) + ".png")

    # shrink image by absolute scale
    img2 = shrink(img2, scale[0])

    max_coord = (img1.size[0]-img2.size[0], img1.size[1]-img2.size[1])

    # create and save image
    for i in range(n):
        # random range of coordinates c1 ~ c2
        random_coord = (random.randint(start_coord[0], max_coord[0]), random.randint(start_coord[1], max_coord[1]))

        # scale image by y coordinate
        obj = shrink(img2, (img1.size[1] / (random_coord[1] + img2.size[1])) ** scale[1])

        # place img2 (obj) onto img1
        img = place_image(img1, obj, random_coord, flip)
        filename = str(mushroom) + '-' + str(background) + "_" + str(i) + '.jpg'
        # img.save(path + '/' + filename)
        img.save(path + "/images" + '/' + filename)

        # create and save dataframe
        data = [filename, "mushroom", img.size[0], img.size[1], random_coord[0], random_coord[1], random_coord[0] + obj.size[0], random_coord[1] + obj.size[1]]
        s = pd.Series(data, index=df.columns)
        pd.concat([df, s], ignore_index=True)

        # create yolo annotation
        filename = str(mushroom) + '-' + str(background) + "_" + str(i) + '.txt'
        create_yolo_ann(path + "/labels", filename, 0, random_coord, obj.size, img.size)
    return df

# add mulitple mushrooms on background image
# randomly choose 1 mushroom type and add 1- 5 of them
def multiple_mush_on_bg(n, mushroom_num, background, flip, path):

    bg_par = read_bg_par("./nature images/image parameters.txt")
    start_coord = eval(bg_par[background][0])
    scale = eval(bg_par[background][1])

    # Opening background image (used in background)
    img1 = Image.open("./nature images/" + str(background) + ".jpg")
    
    # Opening mushroom images (overlay image)
    mushroom_images = dict()
        
    
    for mushroom in range(mushroom_num):
        img2 = Image.open("./mushroom images/" + str(mushroom + 1) + ".png")

        # shrink image by absolute scale
        img2 = shrink(img2, scale[0])
        mushroom_images[mushroom + 1] = img2


    # create and save image
    for i in range(n):
        mushroom = random.randint(1, mushroom_num)
        img = img1
        filename = str(mushroom)
        annotation_filename = filename + '-' + str(background) + "_" + str(i) + '.txt'
        image_filename = filename + '-' + str(background) + "_" + str(i) + '.jpg'
   
        img2 = mushroom_images[mushroom]
        max_coord = (img1.size[0]-img2.size[0], img1.size[1]-img2.size[1])
        
        # merge 1 - 5 mushrooms
        for i in range(random.randint(1, 6)):    
            # random range of coordinates c1 ~ c2
            
            random_coord = (random.randint(start_coord[0], max_coord[0]), random.randint(start_coord[1], max_coord[1]))

            # scale image by y coordinate
            obj = shrink(img2, (img1.size[1] / (random_coord[1] + img2.size[1])) ** scale[1])

            # place img2 (obj) onto img1
            img = place_image(img, obj, random_coord, flip)
            
            # create yolo annotation
            create_yolo_ann(path + "/labels", annotation_filename, 0, random_coord, obj.size, img.size)


        img.save(path + "/images" + '/' + image_filename)

# old version
# if m_dict is integer (number of mushrooms), create random dict
def multiple_mush_on_bg_v1(n, m_dict, background, flip, path):

    bg_par = read_bg_par("./nature images/image parameters.txt")
    start_coord = eval(bg_par[background][0])
    scale = eval(bg_par[background][1])

    # Opening background image (used in background)
    img1 = Image.open("./nature images/" + str(background) + ".jpg")
    
    rand_dict = isinstance(m_dict, int)
    mushroom_num = m_dict

    # create and save image
    for i in range(n):

        # if m_dict is integer (number of mushrooms), create random dict
        if rand_dict:
            m_dict = dict()
            for key in range(mushroom_num):
                m_dict[key+1] = random.randint(0,2)
                # if m_dict[key+1] == 0:
                #     del m_dict[key+1]

    
        mushroom_images = dict()
        # Opening mushroom images (overlay image)
        for mushroom in m_dict:
            img2 = Image.open("./mushroom images/" + str(mushroom) + ".png")

            # shrink image by absolute scale
            img2 = shrink(img2, scale[0])
            mushroom_images[mushroom] = img2


        # get filename of created image / annotation
        filename = ''
        for mushroom in m_dict:
            if m_dict[mushroom] != 0:
                if filename == '':
                    filename += str(mushroom)
                else:
                    filename += ',' + str(mushroom)

        img = img1
        annotation_filename = filename + '-' + str(background) + "_" + str(i) + '.txt'
        image_filename = filename + '-' + str(background) + "_" + str(i) + '.jpg'

        for mushroom in m_dict:
            img2 = mushroom_images[mushroom]
            max_coord = (img1.size[0]-img2.size[0], img1.size[1]-img2.size[1])
            
            for i in range(m_dict[mushroom]):    
                # random range of coordinates c1 ~ c2
                
                random_coord = (random.randint(start_coord[0], max_coord[0]), random.randint(start_coord[1], max_coord[1]))

                # scale image by y coordinate
                obj = shrink(img2, (img1.size[1] / (random_coord[1] + img2.size[1])) ** scale[1])

                # place img2 (obj) onto img1
                img = place_image(img, obj, random_coord, flip)
                
                # create yolo annotation
                create_yolo_ann(path + "/labels", annotation_filename, 0, random_coord, obj.size, img.size)


        img.save(path + "/images" + '/' + image_filename)


# returns background images' parameters as a dict
def read_bg_par(path):
    # key = mushroom number, value = mushroom's parameters
    bg_parameters = dict()

    # background parameters
    file = open(path, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):        
        bg_parameters[i + 1] = re.findall('\(([^)]+)', line)

    return bg_parameters


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


# creates yolo annotations
def create_yolo_ann(folder_path, filename, class_id, bb_coord, bb_size, img_size):

    x, y = bb_coord
    w, h = bb_size
    img_w, img_h = img_size

    # Finding midpoints
    x_centre = (x + (x+w))/2
    y_centre = (y + (y+h))/2
    
    # Normalization
    x_centre = x_centre / img_w
    y_centre = y_centre / img_h
    w = w / img_w
    h = h / img_h

    # Limiting upto fix number of decimal places
    x_centre = format(x_centre, '.6f')
    y_centre = format(y_centre, '.6f')
    w = format(w, '.6f')
    h = format(h, '.6f')
    
    ann_file = open(f"{folder_path}/{filename}", "a")
    ann_file.write(f"0 {x_centre} {y_centre} {w} {h}\n")
    ann_file.close()

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
