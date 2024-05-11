"""Acting like a session database """
import base64
import os

from Server.data.recordings import Recording


def embed_record(file_path):
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"File {file_path} not found")


class DataStorage:
    def __init__(self):
        self.profiles = set()
        self.recordings = set()
        self.attacks = set()

    def add_profile(self, profile):
        print("New profile added: {}".format(profile))
        self.profiles.add(profile)
        print(self.profiles)

    def add_attack(self, new_attack):
        self.attacks.add(new_attack)

    def get_attacks(self):
        return self.attacks

    def get_profiles(self):
        return self.profiles

    def add_recording(self, recording):
        self.recordings.add(recording)

    def get_recordings(self):
        return self.recordings

    def update_records_list(self, dir_name):
        for file in os.listdir(dir_name):
            if file.endswith('.mp3'):
                file_path = os.path.join(dir_name, file)  # Full path to the file
                rec = Recording(full_path=file_path, embedd_rec=embed_record(file_path),
                                file_name=file)
                self.recordings.add(rec)
