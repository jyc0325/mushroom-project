from PIL import Image

# resize image (shrink) by a scale factor s
def shrink(img, s):
    size = (int(img.size[0] / s), int(img.size[1] / s))
    return img.resize(size)

img_path = "./mushroom images/4_original.png"

img = Image.open(img_path)
i = Image.open("./mushroom images/1.png")
print(img.size)
print(i.size)

img2 = shrink(img, 4)
img2.save("./mushroom images/4.png")
print(img2.size)