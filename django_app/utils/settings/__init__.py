import json
import os


def get_config():
    # 1. .conf폴더의 settings_local.json을 읽어온다.
    current_file_path = os.path.abspath(__file__)
    path_dir_settings = os.path.dirname(current_file_path)
    path_dir_utils = os.path.dirname(path_dir_settings)

    path_dir_base = os.path.dirname(path_dir_utils)
    path_dir_root = os.path.dirname(path_dir_base)
    path_dir_conf = os.path.join(path_dir_root, '.conf')
    path_settings_local = os.path.join(path_dir_conf, 'settings_local.json')

    # 2. 해당 내용을 json.loads()을 이용해서 str-> dict형태로 변환
    with open(path_settings_local, 'r') as f:
        config_json = f.read()

    config = json.loads(config_json)
    return config
