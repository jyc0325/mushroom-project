from image_merge import *
import shutil
import os

# merge mushroom image img2 on background image img1 as image file "img1-img2"
# n: number of images to create
def merge_manual(n, mushroom, background, scale, start_coord, flip):
    # # Opening background image (used in background)
    # img1 = Image.open("./nature images/" + str(b) + ".jpg")
    
    # # Opening mushroom image (overlay image)
    # img2 = Image.open("./mushroom images/" + str(b) + ".png")

    output_folder = "./created_images"

    # output_folder = "./created_images/" + str(mushroom) + "-" + str(background)
    if not path.exists(output_folder + "/images"):
        mkdir(output_folder + "/images")
    if not path.exists(output_folder + "/labels"):
        mkdir(output_folder + "/labels")

    df = mush_on_bg(n, mushroom, background, scale, start_coord, flip, output_folder)
    # df.to_csv(output_folder + '/data.csv', index=False)
    # csv_to_coco(output_folder + "/data.csv", output_folder)

# merge multiple mushrooms onto background
# number of mushrooms specifed by dict; key = mushroom number, value = number of mushrooms
def merge(n, m_dict, background, flip):
    output_folder = "./created_images"

    # output_folder = "./created_images/" + str(mushroom) + "-" + str(background)
    if not path.exists(output_folder + "/images"):
        mkdir(output_folder + "/images")
    if not path.exists(output_folder + "/labels"):
        mkdir(output_folder + "/labels")

    multiple_mush_on_bg(n, m_dict, background, flip, output_folder)
    



def delete_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    # delete contents of folder
    delete_files("./created_images")

    # mushroom number , background number

    # merge_manual(100, 3, 2, (2, 2), (150, 720), True)

    m_dict = {1:1, 2:2, 3:1}
    merge(100,{1:3, 3:2, 5:4}, 5, True)