import os
from PIL import Image

dir = './mushroom images/'

for count, file in enumerate(os.listdir(dir)):
    image = Image.open(dir + file)
    width, height = image.size

    # make bigger side's length 150; match other side's length while maintaining ratio
    if width > height:
        height = int(height * 150 / width)
        width = 150
    else:
        width = int(width * 150 / height)
        height = 150

    image = image.resize((width, height))
    image.save(dir + str(count + 1) + '.png')
