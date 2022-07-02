import os, json
from collections import Counter

path_to_json = '/home/ahmet/Desktop/MoveFilesTest/cornetto_ask_atesi_second/'

Elements = []

for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
    with open(path_to_json + file_name) as json_file:
        data = json.load(json_file)
    for cnt in data['shapes']:
        Elements.append(cnt['label'])
    else:continue
print("LabelNames & Total Counts: ", data['shapes'][0]['label'], ": Total Labels", Counter(Elements))

