# coding=utf-8
import json
import math
# import pymysql
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


def get_url(region, page):
    parameterList = [
        'https://api.map.baidu.com/place/v2/search?',
        'query=图书馆',
        '&tag=图书馆',
        '&region={0}'.format(region),
        '&city_limit=true',
        '&output=json',
        '&scope=2',
        '&page_size=20',
        '&page_num={0}'.format(page),
        '&ak=99AO36G6CGA1sdePauND5vzral0iMgRA'
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
        print('get html text异常捕获', result)
        return ''


def get_data(result):
    try:
        name = result['name']
        lat = result['location']['lat']
        lng = result['location']['lng']
        address = result['address']
        province = result['province']
        city = result['city']
        area = result['area']
        # telephone = result['telephone']
        uid = result['uid']
        tag = result['detail_info']['tag']
        tagList = tag.split(';')
        if len(tagList) == 1:
            tag1, tag2 = [tag, '其他']
        else:
            tag1, tag2 = tagList
    except Exception as r:
        print('get data异常捕获', r)
        print(result)
        tag1, tag2 = ['其他', '其他']
    finally:
        lon, lat = tf.bd09_to_wgs84(lng, lat)
        return [name, lat, lng, address, province, city, area, uid, tag1, tag2]

def main():
    path = '部分县区.txt'
    with open(path, 'r+', encoding='utf-8') as f:
        area_list = f.readlines()
    f.close()

    # # 连接数据库
    # db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    # print('数据库连接成功')
    # cur = db.cursor()
    # sql = 'INSERT INTO 图书馆_copy1(name, lat, lng, address, province, city, area, uid, tag1, tag2)VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    # for a in area_list:
    #     a = a.replace('\n', '')
    #     # print(a)
    #     url = get_url(a, 0)
    #     html = get_html_text(url)
    #     output_json = json.loads(html)
    #     total_count = output_json['total']
    #     result_type = output_json['result_type']
    #     if total_count == 0 or result_type != 'poi_type':
    #         continue
    #     pass
    #     print(a, total_count)
    #     for i in range(math.ceil(total_count/20)):
    #         url = get_url(a, i)
    #         html = get_html_text(url)
    #         output_json = json.loads(html)
    #         results = output_json['results']
            
    #         for r in results:
    #             data = get_data(r)
    #             try:
    #                 # print(d[0], '获取正常')
    #                 value = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
    #                 cur.execute(sql, value)
    #                 db.commit()
    #             except pymysql.Error as result:
    #                 print('插入失败：' + str(result))
    #                 db.rollback()
    #         pass

    path = 'poi检索.csv'
    with open(path, 'w+', encoding='utf-8') as f:
        f.write('name,lat,lng,address,province,city,area,uid,tag1,tag2\n')
        for a in area_list:
            a = a.replace('\n', '')
            url = get_url(a, 0)
            html = get_html_text(url)
            output_json = json.loads(html)
            total_count = output_json['total']
            result_type = output_json['result_type']
            if total_count == 0 or result_type != 'poi_type':
                continue
            pass
            print(a, total_count)
            for i in range(math.ceil(total_count/20)):
                url = get_url(a, i)
                html = get_html_text(url)
                output_json = json.loads(html)
                results = output_json['results']

                for r in results:
                    data = get_data(r)
                    f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'
                    .format(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
                pass
    f.close()
    pass


if __name__ == '__main__':
    main()
