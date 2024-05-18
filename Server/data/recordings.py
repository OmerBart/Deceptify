"""
This Recoding object stores the recording information, and can be transfer to the
remote server easily using to_json() and from_json() methods.
"""
import json
import numpy as np
from pydub import AudioSegment

from Server.data.audio import bytes_to_array


class Recording:
    def __init__(self, full_path, record_in_bytes, file_name):
        """
        :param full_path: The full path to the recording file
        :param record_in_bytes: The recording data in bytes
        :param file_name: The name of the recording file
        """
        self.full_path = full_path
        self.file_name = file_name
        self.record_in_bytes = record_in_bytes
        self.embedd_rec = bytes_to_array(record_in_bytes)

    def get_encoded_recording(self):
        return self.embedd_rec

    def __hash__(self):
        return hash((self.full_path, self.file_name))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.embedd_rec == other.embedd_rec and self.full_path == other.full_path \
            and self.file_name == other.file_name

    def to_dict(self):
        return {
            'embedd_rec': self.embedd_rec,
            'full_path': self.full_path,
            'file_name': self.file_name
        }

    @staticmethod
    def from_dict(d):
        embedd_rec = d['embedd_rec']
        full_path = d['full_path']
        file_name = d['file_name']
        return Recording(embedd_rec, full_path, file_name)

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str):
        return Recording.from_dict(json.loads(json_str))
