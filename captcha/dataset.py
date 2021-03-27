import os
import glob

from PIL import Image
from common import *


CAPTCHA_IMAGE_FOLDER = "captcha"
OUTPUT_FOLDER = "extracted"


# Get a list of all the captcha images we need to process
images = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*.png"))
counts = {}

for (i, img_file) in enumerate(images):
    if i % 100 == 0:
        print("processing image {}/{}, got {}"
              .format(i + 1, len(images), sum(counts.values())))
    labels = os.path.splitext(os.path.basename(img_file))[0]
    img = Image.open(img_file)
    img = preprocess(img)
    boxes = split_img(img, 5)
    if len(boxes) != len(labels):
        continue
    for box, label in zip(boxes, labels):
        x, y, w, h = box
        box_img = img.crop((x - 2, y - 2, x + w + 2, y + h + 2))
        folder = os.path.join(OUTPUT_FOLDER, label)
        if not os.path.exists(folder):
            os.makedirs(folder)
        count = counts.get(label, 0)
        counts[label] = count + 1
        path = os.path.join(folder, "{:03}.png".format(count))
        box_img.save(path)

print(counts)
