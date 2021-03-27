from .common import *

import os
import sys
import numpy as np
# import tensorflow.lite as tflite
import tflite_runtime.interpreter as tflite

MODEL_FILENAME = "model.tflite"


def recognize(img):
    interpreter = tflite.Interpreter(os.path.join(sys.path[0], MODEL_FILENAME))
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = preprocess(img)
    boxes = split_img(img, 5)
    predictions = []
    for box in boxes:
        x, y, w, h = box
        box_img = img.crop((x - 2, y - 2, x + w + 2, y + h + 2))
        box_img = box_img.resize((20, 20))

        box_img = np.array(box_img, dtype=np.float32)
        # Add a third channel dimension to the image to make Keras happy
        box_img = np.expand_dims(box_img, axis=2)
        # Add a batch dimension to fit the interpreter
        box_img = np.expand_dims(box_img, axis=0)

        interpreter.set_tensor(input_details[0]['index'], box_img)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])
        predictions.append(id2label(np.argmax(prediction)))

    return "".join(predictions)


if __name__ == '__main__':
    import sys
    img = Image.open(sys.argv[1])
    print(recognize(img))
