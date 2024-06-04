import enum
import json

import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf
import os


class Predict:
    __models_dir = os.path.join(os.getcwd(), 'models')

    def __init__(self, image_path):
        self.img_path = image_path

    def __predict(self, model):
        image = mpimg.imread(self.img_path)
        image = np.expand_dims(image, axis=0)
        return model.predict(image)

    def __get_classes(self, file_path):
        with open(file_path) as file:
            return [line.rstrip() for line in file]

    def predict(self):
        categories = ["generation", "type1", "type2"]
        predictions = []
        for cat in categories:
            model_path = os.path.join('models', cat, 'best/model.h5')
            class_path = os.path.join('models', cat, 'class_names.txt')
            model = tf.keras.models.load_model(model_path)
            class_names = self.__get_classes(class_path)
            result = self.__predict(model)[0]
            prediction = {class_names[i]: str(result[i]) for i in range(len(result))}
            predictions.append((cat, prediction))
        print(predictions)
        return dict(predictions)
