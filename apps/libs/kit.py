# -*- coding: utf-8 -*-
import os, time, re, requests, json

def current_milli_time():
    return int(round(time.time()))

def time_format(stamp, pattern = "%Y-%m-%d %H:%M:%S"):
    return time.strftime(pattern, time.localtime(stamp))

def str_include(keywords, origin):
    return origin.find(keywords) > -1

def write_json_to_file(file_path, data):
    try:
        with open(file_path, 'w') as f:
            f.write(json.dumps(data))
        return True, None
    except Exception as e:
        return False, e

def get_json_from_file(file_path):
    data = None
    try:
        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.loads(f.read())
        return data, None
    except Exception as e:
        return None, e

def is_exists(file_path):
    return os.path.exists(file_path)

def remove_file(file_path):
    if is_exists(file_path):
        os.remove(file_path)

def download(url, encoding = 'utf-8'):
    UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
    header = { "User-Agent" : UA }
    r = requests.get(url, headers = header)
    r.encoding = encoding
    return r.text

def download_file(url, file_path):
    UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
    header = { "User-Agent" : UA }
    r = requests.get(url, headers = header)
    with open(file_path, 'wb') as fd:
        for chunk in r.iter_content(1024):
            fd.write(chunk)

def str_search(origin_str, regex):
    m = regex.search(origin_str)
    if m:
        return m.group(0)
    return False