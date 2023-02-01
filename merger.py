from image_merge import *

# merge mushroom image img2 on background image img1 as image file a-b
# n: number of images to create

def merge(n, mushroom, background, scale, start_coord, flip):
    # # Opening background image (used in background)
    # img1 = Image.open("./nature images/" + str(b) + ".jpg")
    
    # # Opening mushroom image (overlay image)
    # img2 = Image.open("./mushroom images/" + str(b) + ".png")

    

    output_folder = "./created_images/" + str(mushroom) + "-" + str(background)
    if not path.exists(output_folder):
        mkdir(output_folder)
    if not path.exists(output_folder + "_labels"):
        mkdir(output_folder + "_labels")

    df = create_save_images(n, mushroom, background, scale, start_coord, flip, output_folder)
    df.to_csv(output_folder + '/data.csv', index=False)
    csv_to_coco(output_folder + "/data.csv", output_folder)



if __name__ == "__main__":
    merge(10, 1, 1, (1.5, 2), (0, 353), True)
    merge(10, 2, 1, (1.5, 2), (0, 353), True)
    merge(10, 3, 1, (1.5, 2), (0, 353), True)
    merge(10, 1, 2, (2, 2), (0, 456), True)
    merge(10, 2, 2, (2, 2), (0, 456), True)
    merge(10, 3, 2, (2, 2), (0, 456), True)