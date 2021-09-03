from wanikani_api.client import Client

wanikani_key = key_v2 = "c882070c-b9c6-4894-b962-afab421d09af"
v2_api_key = wanikani_key
client = Client(v2_api_key, subject_cache_enabled=True)

rad_list = []

user_info = client.user_information()
level = user_info.level

radicals = client.subjects(levels=1, types='radical')

for radical in radicals:
    rad_list.append(radical.id)

subjects = {}


def generate_items():
    for id_subject in rad_list:
        subject = client.subject(id_subject)
        if subject.characters is not None:
            subjects[str(id_subject)] = [subject.characters]
    return subjects


subject = generate_items()
print(subjects)
