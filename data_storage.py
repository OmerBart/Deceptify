"""Acting like a session database """


class DataStorage:
    def __init__(self):
        self.profiles = []

    def add_profile(self, profile):
        print("New profile added: {}".format(profile))
        self.profiles.append(profile)
        print(self.profiles)

    def get_profiles(self):
        return self.profiles
