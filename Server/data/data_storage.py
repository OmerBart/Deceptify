"""
Acting like a session database,
Stores all the current information of the client, new attacks, profiles, recordings, etc.
After the session ends, this object will push all the information to the remote server to
save that in the database.
"""
import base64
import json
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
        self.videos = set()
        self.images = set()

    def add_image(self, image):
        self.images.add(image)

    def get_images(self):
        return self.images

    def add_video(self, video):
        self.videos.add(video)

    def get_videos(self):
        return self.videos

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
                rec = Recording(full_path=file_path, record_in_bytes=embed_record(file_path),
                                file_name=file)
                self.recordings.add(rec)

    def prepare_data_to_remote_server(self):
        """Prepare the data before sending to the remote server."""
        audios = [audio.to_json() for audio in self.recordings]
        videos = [video.to_json() for video in self.videos]
        profiles = [profile.to_json() for profile in self.profiles]
        images = [img.to_json() for img in self.images]
        return json.dumps({
            'audios': audios,
            'videos': videos,
            'profiles': profiles,
            'images': images
        })
