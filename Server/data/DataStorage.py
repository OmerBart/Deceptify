"""
Acting like a session database,
Stores all the current information of the client, new attacks, profiles, recordings, etc.
After the session ends, this object will push all the information to the remote server to
save that in the database.
"""
import base64
import json
import os
from Server.data.Profile import Profile
from typing import Set, List
from Server.data.recordings import Recording


def embed_record(file_path):
    try:
        with open(file_path, 'rb') as file:
            return bytearray(base64.b64encode(file.read()))
    except FileNotFoundError:
        print(f"File {file_path} not found")


class DataStorage:
    """
    A class that represents the data storage for profiles, prompts, and attacks.
    """

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self.profiles = set()
            self.recordings = set()
            self.videos = set()
            self.images = set()
            self.prompts = set()
            self.attacks = set()

    def add_image(self, image):
        self.images.add(image)

    def get_images(self):
        return self.images

    def add_video(self, video):
        self.videos.add(video)

    def get_videos(self):
        return self.videos

    def add_prompt(self, prompt):
        """
        Add a prompt to the data storage.

        Args:
            prompt: The prompt to be added.
        """
        self.prompts.add(prompt)

    def get_prompts(self):
        """
        Get all the prompts stored in the data storage.

        Returns:
            A set of prompts.
        """
        return self.prompts

    def delete_prompt(self, desc):
        prompt = None
        for prt in self.prompts:
            if prt.prompt_desc == desc:
                prompt = prt
        self.prompts.remove(prompt)

    def add_profile(self, profile):
        """
        Add a profile to the data storage.

        Args:
            profile: The profile to be added.
        """
        self.profiles.add(profile)

    def add_attack(self, new_attack):
        """
        Add an attack to the data storage.
        This also adds the attack to the target and victim profiles.

        Args:
            new_attack: The attack to be added.
        """

        target = new_attack.get_target()
        victim = new_attack.get_mimic_profile()
        target.addAttack(new_attack)
        victim.addAttack(new_attack)
        self.attacks.add(new_attack)

    def get_attacks(self):
        """
        Get all the attacks stored in the data storage.

        Returns:
            A set of attacks.
        """
        return self.attacks

    def delete_attack(self, attackID):
        """
        Delete an attack from the data storage.

        Args:
            attackID: The ID of the attack to be deleted.
        """
        attack_to_remove = None
        for attack in self.attacks:
            if attack.getID() == attackID:
                attack_to_remove = attack
                break
        if attack_to_remove:
            self.attacks.remove(attack_to_remove)

    def get_AllProfiles(self) -> Set[Profile]:
        """
        Get all the profiles stored in the data storage.

        Returns:
            A set of profiles.
        """
        return self.profiles

    def get_profiles(self, attacker: bool = False) -> Set[Profile]:
        """
        Get the profiles stored in the data storage according to role.

        Args:
            attacker: A boolean indicating whether to get attacker profiles or victim profiles.

        Returns:
            A set of profiles.
        """
        if attacker:
            return [profile for profile in self.profiles if profile.role == "Attacker"]
        else:
            return [profile for profile in self.profiles if profile.role == "Victim"]

    def getAllProfileNames(self) -> List[str]:
        """
        Get the names of all the profiles stored in the data storage.

        Returns:
            A list of profile names or if empty a message.
        """
        if len(self.profiles) == 0:
            return ["No profiles available, time to create some!"]
        else:
            return [profile.getName() for profile in self.profiles]

    def get_profile(self, profile_name) -> Profile | None:
        """
        Get a profile from the data storage by its name.

        Args:
            profile_name: The name of the profile.

        Returns:
            The profile object if found, None otherwise.
        """
        for profile in self.profiles:
            if profile.getName() == profile_name:
                return profile
        return None

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
        """
        Prepare the data before sending it to the remote server.

        Returns:
            A JSON string containing the profiles and prompts data.
        """
        audios = [audio.to_json() for audio in self.recordings]
        videos = [video.to_json() for video in self.videos]
        profiles = [profile.to_json() for profile in self.profiles]
        prompts = [prompt.to_json() for prompt in self.prompts]
        images = [img.to_json() for img in self.images]
        return json.dumps({
            'audios': audios,
            'videos': videos,
            'profiles': profiles,
            'prompts': prompts,
            'images': images
        })
