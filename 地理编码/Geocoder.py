import json
import requests
import transform_location as tf


def get_location(address):
    """
    正 地理编码
    服务文档: http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
    :param address: 待解析的地址
    :return: [经度, 纬度, 状态码, 描述地址理解程度]
    """
    try:
        ak = "99AO36G6CGA1sdePauND5vzral0iMgRA"  # 百度开发者ak
        coordtype = "bd09ll"  # 坐标系
        # 构建 URL
        url = "http://api.map.baidu.com/geocoding/v3/?address=" + address + "&output=json&ak=" + ak + "&ret_coordtype=" + coordtype

        text = requests.get(url, verify=False).text
        # print(text)
        location_info = json.loads(text)
        if location_info["status"] != 0:
            return [0, 0, 1, 0]
        status = location_info["status"]
        lng = location_info["result"]["location"]["lng"]
        lat = location_info["result"]["location"]["lat"]
        comprehension = location_info["result"]["comprehension"]
        # print(lng, lat)
        lng, lat = tf.bd09_to_wgs84(lng, lat)  # BD-09转WGS84
        return [lng, lat, status, comprehension]
    except Exception as result:
        print("异常捕获：", result)
        return [0, 0, 1, 0]


def main():
    address = ''
    location = get_location(address)
    print(location)
    print("wgs84:",location[0], location[1])
    pass


if __name__ == '__main__':
    main()
