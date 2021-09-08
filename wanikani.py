from wanikani_api.client import Client
from time import time

# TODO: picklize all the things
# TODO: cache data, eg. radicals, timestamp - check if older than 24h
# Make a sync screen

wanikani_key = key_v2 = "c882070c-b9c6-4894-b962-afab421d09af"
v2_api_key = wanikani_key

expiry_time = 86400  # 24h
now_time = round(time())
data_time = 1631078705

if (now_time - data_time) < expiry_time:
    cache = True
else:
    cache = False  # force sync

rad_list = []
subjects = {}

if not cache:
    client = Client(v2_api_key, subject_cache_enabled=True)
    user_info = client.user_information()
    level = user_info.level
    radicals = client.subjects(levels=level, types='radical')

    for radical in radicals:
        rad_list.append(radical.id)


# TODO: this wants to be automagic
rad_list.insert(0, '')
level = 1
rad_list.insert(level, {'1': ['一'],
                        '2': ['ハ'],
                        '3': ['丶'],
                        '4': ['七'],
                        '5': ['丿'],
                        '6': ['亅'],
                        '7': ['二'],
                        '8': ['亠'],
                        '9': ['人'],
                        '10': ['ト'],
                        '11': ['九'],
                        '12': ['入'],
                        '13': ['力'],
                        '14': ['勹'],
                        '15': ['十'],
                        '16': ['口'],
                        '18': ['大'],
                        '19': ['女'],
                        '20': ['山'],
                        '21': ['川'],
                        '22': ['日'],
                        '23': ['木'],
                        '25': ['工']})
level = 11
rad_list.insert(level, {'189': ['令'],
                        '190': ['申'],
                        '191': ['兄'],
                        '193': ['及'],
                        '194': ['戈'],
                        '195': ['皮'],
                        '196': ['艮'],
                        '197': ['音'],
                        '198': ['少'],
                        '199': ['単']})


def generate_items():
    for id_subject in rad_list:
        subj = client.subject(id_subject)
        if subj.characters is not None:
            subjects[str(id_subject)] = [subj.characters]
    return subjects

# subjects = generate_items()
# print(subjects)
