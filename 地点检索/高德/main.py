#coding=utf-8
import GeoCode as geo


def main():
    path = '省市.txt'
    with open(path, 'r+', encoding='utf-8') as f:
        area_list = f.readlines()
    f.close()

    path = '全国省市adcode对应表.csv'
    with open(path, 'w+', encoding='utf-8') as f:
        # f.write()
        for a in area_list:
            a = a.replace('\n','')
            adcode = geo.get_adcode(a)
            print(a, adcode)
            f.write('{0},{1}\n'.format(a, adcode))
    f.close()


if __name__ == "__main__":
    main()
