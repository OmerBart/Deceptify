import json

import numpy as np
import cv2


class Image:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self.image = cv2.imread(path)
        self.image_embedded = np.array(self.image)

    def show(self):
        cv2.imshow(self.filename, self.image_embedded)

    def to_dict(self):
        return {
            'filename': self.filename,
            'image': self.image_embedded,
            'path': self.path
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(d):
        return Image(d.get('path'), d.get('filename'))

    @staticmethod
    def from_json(json_str):
        return Image(json_str.get('path'), json_str.get('filename'))

    def __eq__(self, other):
        return self.image_embedded == other.image_embedded

    def __hash__(self):
        return hash(self.image_embedded)
