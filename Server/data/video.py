import json
import cv2

import numpy as np


# TODO: WHEN THE TIME WILL COME, CHECK THIS FUNCTION.
def video_embedded(video_path):  # Given a video path, embedd it.
    print(video_path)
    cap = cv2.VideoCapture(video_path)
    frames = [np.array(frame) for ret, frame in iter(lambda: cap.read(), (False, None))]
    cap.release()
    return np.stack(frames, axis=0)


class Video:
    def __init__(self, video_path, video_filename):
        """
        :param video_path: The path of the video.
        :param video_filename: The name of the video.
        """
        self.video_path = video_path
        self.video_filename = video_filename
        self.video_embedded = video_embedded(self.video_path)  # numpy array representation,
        # for the model at the time.

    def to_dict(self):
        return {
            'video_path': self.video_path,
            'video_filename': self.video_filename,
            'video_embedded': self.video_embedded,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(d):
        return Video(**d)

    @staticmethod
    def from_json(d):
        return Video.from_dict(json.loads(d))

    def __eq__(self, other):
        return self.video_in_bytes == other.video_in_bytes and \
            self.video_embedded == other.video_embedded

    def __hash__(self):
        return hash(self.video_in_bytes)
