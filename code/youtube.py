import json
import os
from pprint import pprint

import requests

current_file_path = os.path.abspath(__file__)
go_to_parent_path = os.path.dirname(current_file_path)
go_to_child_path_or_file = os.path.join(go_to_parent_path, 'youtube.py')
print(go_to_parent_path)
print(go_to_child_path_or_file)

# 1. .conf폴더의 settings_local.json을 읽어온다.
current_file_path = os.path.abspath(__file__)
path_dir_code = os.path.dirname(current_file_path)
path_dir_youtube = os.path.dirname(path_dir_code)
path_dir_conf = os.path.join(path_dir_youtube, '.conf')
path_settings_local = os.path.join(path_dir_conf, 'settings_local.json')

# 2. 해당 내용을 json.loads()을 이용해서 str-> dict형태로 변환
with open(path_settings_local, 'r') as f:
    json_api_key = f.read()

api_key = json.loads(json_api_key)
youtube_api_key = api_key['youtube']['API_KEY']

# 3. requests 라이브러리를 이용 (pip install requests), get요청으로 데이터를 받아온 후
params = {
    'part': 'snippet',
    'q': '강아지',
    'maxResults': 50,
    'key': youtube_api_key,
    'type': 'video'
}

r = requests.get('https://www.googleapis.com/youtube/v3/search?', params=params)
result = r.text
# 4. 해당 내용을 다시 파이썬 객체로 변환
result_dict = json.loads(result)
pprint(result_dict)
# 5. 이후 내부에 있는 검색결과를 적절히 루프하며 프린트 해주기
items = result_dict['items']
for index, item in enumerate(items):
    video_id = item['id']['videoId']
    title = item['snippet']['title']
    description = item['snippet']['description']
    print(index + 1, title, description, video_id)


# file_settings_local = open(settings_local)
# dict_api_key = json.loads(file_settings_local.read())
# file_settings_local.close()
# key = dict_api_key['youtube']['API_KEY']
