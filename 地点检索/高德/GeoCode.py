# coding=utf-8
import json
import time
import math
import pprint
import pymysql
import requests
import transform_location as tf

# 数据库配置
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = 'shiaohan'
DBNAME = 'db_test'

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'
}


def get_url(address):
    parameterList = [
        'https://restapi.amap.com/v3/geocode/geo?',
        'key=fb3116d44cafd781636f1d84d4758e5f',
        '&address={0}'.format(address),
        '&output=JSON'
    ]
    url = ''.join(parameterList)
    return url


def get_html_text(url):  # 获取网页内容
    try:
        r = requests.post(url, headers=Headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as result:
        print('异常捕获', result)
        return ''


def get_adcode(address):
    url = get_url(address)
    html = get_html_text(url)
    output_json = json.loads(html)
    geocodes = output_json['geocodes']

    adcode = geocodes[0]['adcode']
    return adcode


def main():
    address = '洛阳市'
    url = get_url(address)
    html = get_html_text(url)
    output_json = json.loads(html)
    pprint.pprint(output_json)
    geocodes = output_json['geocodes']

    adcode = geocodes[0]['adcode']
    city = geocodes[0]['city']
    citycode = geocodes[0]['citycode']
    district = geocodes[0]['district']
    formatted_address = geocodes[0]['formatted_address']
    level = geocodes[0]['level']
    location = geocodes[0]['location']
    province = geocodes[0]['province']

    longitude, latitude = location.split(',')
    longitude = float(longitude)
    latitude = float(latitude)
    longitude, latitude = tf.gcj02_to_wgs84(longitude, latitude)
    print(adcode, city, citycode, district, formatted_address, level, province, latitude, longitude)
    pass


if __name__ == '__main__':
    main()
