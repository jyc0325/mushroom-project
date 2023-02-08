from image_merge import *
import shutil
import os

# merge mushroom image img2 on background image img1 as image file a-b
# n: number of images to create

def merge(n, mushroom, background, scale, start_coord, flip):
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

    df = create_save_images(n, mushroom, background, scale, start_coord, flip, output_folder)
    # df.to_csv(output_folder + '/data.csv', index=False)
    # csv_to_coco(output_folder + "/data.csv", output_folder)


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

    # (number of images, mushroom #, background #)
    # merge(100, 1, 1, (0.4, 2), (0, 0), True) # (1.5, 2) , (0, 353)
    # merge(100, 2, 1, (0.4, 2), (0, 0), True)
    # merge(100, 3, 1, (0.4, 2), (0, 0), True)
    # merge(100, 4, 1, (0.4, 2), (0, 0), True)
    # merge(100, 5, 1, (0.4, 2), (0, 0), True)

    # merge(100, 1, 2, (0.3, 2), (0, 0), True)  # (2, 2) , (0, 456)
    # merge(100, 2, 2, (0.3, 2), (0, 0), True)
    # merge(100, 3, 2, (0.3, 2), (0, 0), True)
    # merge(100, 4, 2, (0.3, 2), (0, 0), True)
    # merge(100, 5, 2, (0.3, 2), (0, 0), True)

    merge(100, 1, 1, (1.5, 2), (0, 353), True)
    merge(100, 2, 1, (1.5, 2), (0, 353), True)
    merge(100, 3, 1, (1.5, 2), (0, 353), True)
    merge(100, 4, 1, (1.5, 2), (0, 353), True)
    merge(100, 5, 1, (1.5, 2), (0, 353), True)

    merge(100, 1, 2, (2, 2), (0, 456), True)
    merge(100, 2, 2, (2, 2), (0, 456), True)
    merge(100, 3, 2, (2, 2), (0, 456), True)
    merge(100, 4, 2, (2, 2), (0, 456), True)
    merge(100, 5, 2, (2, 2), (0, 456), True)