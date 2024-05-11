import json


class Attack:
    def __init__(self, campaign_name, mimic_profile, target, description, camp_id):
        self.campaign_name = campaign_name
        self.mimic_profile = mimic_profile
        self.target = target
        self.description = description
        self.id = camp_id

    def to_dict(self):
        return {
            'campaign_name': self.campaign_name,
            'mimic_profile': self.mimic_profile,
            'target': self.target,
            'description': self.description,
            'id': self.id
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        campaign_name = data['campaign_name']
        mimic_profile = data['mimic_profile']
        target = data['target']
        description = data['description']
        camp_id = data['id']
        return Attack(campaign_name, mimic_profile, target, description, camp_id)

    @staticmethod
    def from_json(json_data):
        return Attack.from_dict(json.loads(json_data))

    def __hash__(self):
        return hash((self.campaign_name, self.mimic_profile, self.target, self.description, self.id))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.campaign_name, self.mimic_profile, self.target, self.description, self.id) == \
            (other.campaign_name, other.mimic_profile, other.target, other.description)


# TODO: CONTINUE THIS VOICE_ATTACK IMPLEMENTATION.
class Voice_Attack(Attack):
    def __init__(self, campaign_name, mimic_profile, target, description, camp_id, recordings, transcript=None):
        super().__init__(campaign_name, mimic_profile, target, description, camp_id)
        self.recordings = recordings
        self.transcript = transcript

    def to_dict(self):
        super_dict = self.to_dict()
        super_dict['recordings'] = self.recordings
        if self.transcript:
            super_dict['transcript'] = self.transcript
        return super_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        campaign_name = data['campaign_name']
        mimic_profile = data['mimic_profile']
        target = data['target']
        description = data['description']
        camp_id = data['id']
        recordings = data['recordings']
        transcript = data['transcript']
        return Voice_Attack(campaign_name, mimic_profile, target, description, camp_id,
                            recordings, transcript)

    @staticmethod
    def from_json(json_data):
        return Voice_Attack.from_dict(json.loads(json_data))

    def __hash__(self):
        return hash((self.campaign_name, self.mimic_profile, self.target, self.description, self.id,
                     self.recordings, self.transcript))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.campaign_name, self.mimic_profile, self.target, self.description, self.id, self.transcript,
                self.recordings) == \
            (other.campaign_name, other.mimic_profile, other.target, other.description, other.transcript,
             other.recordings)
