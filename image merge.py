from PIL import Image
import random

# resize image (shrink) by a scale factor s
def shrink(img, s):
    size = (int(img.size[0] / s), int(img.size[1] / s))
    return img.resize(size)

# overlay img2 onto img1 within random range of coordinates c1 ~ c2
def random_place_image(img1, img2, c1=(0,0), c2=(0,0), flip=False):
    random_coord = (random.randint(c1[0], c2[0]), random.randint(c1[1], c2[1]))

    if flip:    # randomly flip image
        flip = random.randint(0, 1)
        if flip:
            img2 = img2.transpose(method=Image.FLIP_LEFT_RIGHT)
            
    # Pasting img2 image on top of copy of img1
    img = img1.copy()
    img.paste(img2, random_coord, mask = img2)
    return img

# create n images by merging img1 and img 2 and save to designated directory
def create_save_images(n, img1, img2, c1, c2, flip, path):
    for i in range(n):
        img = random_place_image(img1, img2, c1, c2, flip)
        img = img.save(path + '/' + str(i) + '.jpg')


if __name__ == "__main__":

    # Opening the primary image (used in background)
    img1 = Image.open(r"floor.jpg")
    
    # Opening the secondary image (overlay image)
    img2 = Image.open(r"./mushroom images/m.png")
    img2 = shrink(img2, 1.5)

    start_coord = (0, 353)
    max_coord = (img1.size[0]-img2.size[0], img1.size[1]-img2.size[1])

    create_save_images(50, img1, img2, start_coord, max_coord, True, "./created_images")

    # img = random_place_image(img1, img2, start_coord, max_coord)
    # img.show()
