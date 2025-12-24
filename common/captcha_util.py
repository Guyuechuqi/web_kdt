import requests
from common.yaml_util import read_config, write_yaml
from config.path import DATA_PATH


def get_captcha():
    params = read_config()["superhawk"]
    return send_requests(**params)

def send_requests(url, username, password, softid, codetype, captcha_pic):
    data = {"user": username, "pass": password, "softid": softid, "codetype": codetype}
    path = DATA_PATH / captcha_pic
    files = {'userfile': open(path, 'rb')}
    response = requests.post(url, files=files, data=data)
    return response.json()["pic_str"]
