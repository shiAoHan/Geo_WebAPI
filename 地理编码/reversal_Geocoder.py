#coding = utf-8
import json
import requests


def get_address(lng, lat):
    """
    逆 地理编码
    服务文档: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
    :param lng, lat: 待解析的经纬度
    :return: [状态码, 国家, 省份, 城市, 城市等级, 描述地址理解程度, 区县名]
    """
    try:
        ak = "99AO36G6CGA1sdePauND5vzral0iMgRA"  # 百度开发者ak
        coordtype = "wgs84ll"  # 坐标系
        # 构建 URL
        url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak="+ak+"&output=json&coordtype="+coordtype+"&location="+str(lat)+","+str(lng)

        text = requests.get(url, verify=False).text
        address_info = json.loads(text)
        if address_info["status"] != 0:
            return [1, "", "", "", "", ""]
        status = address_info["status"]
        country = address_info["result"]["addressComponent"]["country"]
        province = address_info["result"]["addressComponent"]["province"]
        city = address_info["result"]["addressComponent"]["city"]
        city_level = ["country", "province", "city", "district", "town"]
        city_level_id = address_info["result"]["addressComponent"]["city_level"]
        district = address_info["result"]["addressComponent"]["district"]
        # print(lng, lat)
        # lng, lat = tf.bd09_to_wgs84(lng, lat)  # BD-09转WGS84
        return [status, country, province, city, city_level[city_level_id], district]
    except Exception as result:
        print("异常捕获：", result)
        return [1, "", "", "", "", ""]


def main():
    lng = 126.6067189708269
    lat = 45.70709104162458
    address = get_address(lng,lat)
    print(address)
    pass


if __name__ == '__main__':
    main()
