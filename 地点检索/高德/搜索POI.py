# coding=utf-8
import json
import time
import math
import pprint
import pymysql
import requests
import transform_location as tf
import GeoCode as geo

# 数据库配置
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = 'shiaohan'
DBNAME = 'db_test'

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'
}


def get_url(adcode, page):
    keywords = '图书馆'
    types = 140500

    parameterList1 = [  # 搜索POI 1.0
        'https://restapi.amap.com/v3/place/text?',
        'key=bd8424b9bab4b78125d92bd9daa29b7f',
        '&keywords={0}'.format(keywords),
        '&types={0}'.format(types),
        '&city={0}'.format(adcode),
        '&citylimit=true',
        '&offset={0}'.format(25),
        '&page={0}'.format(page),
        # '&extensions=all',
        '&output=JSON'
    ]
    parameterList2 = [  # 搜索POI 2.0
        'https://restapi.amap.com/v5/place/text?',
        'key=bd8424b9bab4b78125d92bd9daa29b7f',
        '&keywords={0}'.format(keywords),
        '&types={0}'.format(types),
        '&region={0}'.format(adcode),
        '&city_limit=true',
        '&page_size={0}'.format(25),
        '&page_num={0}'.format(page),
        '&show_fields=photos',
        '&output=json'
    ]
    url = ''.join(parameterList2)
    return url


def get_html_text(url):  # 获取网页内容
    try:
        r = requests.post(url, headers=Headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as result:
        print('异常捕获get html text:', result)
        return ''


def get_data(poi):
    try:
        name = poi['name']
        location = poi['location']
        address = poi['address'].replace(',', ' ')
        cityname = poi['cityname']
        # photo = poi['photo']
        type = poi['type']
    except Exception as r:
        print('get data异常捕获', r)
        print(poi)
    finally:
        longitude, latitude = location.split(',')
        longitude = float(longitude)
        latitude = float(latitude)
        longitude, latitude = tf.bd09_to_wgs84(longitude, latitude)
        return [name, longitude, latitude, address, cityname, type]


def main():
    path = '全国区县adcode对应表.csv'
    with open(path, 'r', encoding='utf-8') as f:
        area_list = f.readlines()
    f.close()

    path = '全国区县图书馆.csv'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('name,longitude,latitude,address,cityname,type\n')
        
        for a in area_list:
            a = a.replace('\n', '')
            city, adcode = a.split(',')
            page = 1
            while True:
                url = get_url(adcode, page)
                # print(url)
                html = get_html_text(url)
                output_json = json.loads(html)
                # print(output_json)
                count = output_json['count']
                info = output_json['info']
                infocode = output_json['infocode']
                pois = output_json['pois']

                if count == '0':
                    break
                pass
                for p in pois:
                    data = get_data(p)
                    print(data[0], data[1], data[2], data[3], data[4], data[5])
                    f.write('{0},{1},{2},{3},{4},{5}\n'.format(data[0], data[1], data[2], data[3], data[4], data[5]))
                pass
                page = page + 1
            pass
        pass
    f.close()


if __name__ == '__main__':
    main()
