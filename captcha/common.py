import string

import numpy as np
from PIL import Image, ImageFilter

ALL_LABELS = string.digits + string.ascii_lowercase
nb_classes = len(ALL_LABELS)


def split_img(img, space):
    (w, h) = img.size

    def expend(box, pos):
        x, y, w, h = box
        nx, ny = pos
        if x - nx > space or nx - (x + w) > space:
            return None
        if y - ny > space or ny - (y + h) > space:
            return None
        x = min(x, nx)
        y = min(y, ny)
        w = max(w, nx - x)
        h = max(h, ny - y)
        return (x, y, w, h)

    def merge(a, b):
        x1, y1, w1, h1 = a
        x2, y2, w2, h2 = b
        x = min(x1, x2)
        y = min(y1, y2)
        w = max(x1 + w1 - x, x2 + w2 - x)
        h = max(y1 + h1 - y, y2 + h2 - y)
        return (x, y, w, h)

    box = []
    for x in range(w):
        for y in range(h):
            if img.getpixel((x, y)) > 100:
                continue
            remove = []
            newbox = (x, y, 1, 1)
            for b in range(len(box)):
                res = expend(box[b], (x, y))
                if res:
                    remove.append(b)
                    newbox = merge(newbox, box[b])
            for b in reversed(remove):
                box.pop(b)
            box.append(newbox)

    return box


def preprocess(img):
    img = img.convert('1')                          # 二值化
    img = img.filter(ImageFilter.MinFilter(3))      # 膨胀
    # padding
    w, h = img.size
    res = Image.new('1', (w + 20, h + 20), 255)
    res.paste(img, (10, 10))
    return res


def label2id(label):
    return ALL_LABELS.find(label)


def id2label(id):
    return ALL_LABELS[id]


def get_one_hot(targets, nb_classes):
    res = np.eye(nb_classes)[np.array(targets).reshape(-1)]
    return res.reshape(list(targets.shape) + [nb_classes])
