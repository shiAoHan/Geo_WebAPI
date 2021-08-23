# coding = utf-8
import Geocoder
import reversal_Geocoder as rg

def main():
    path = r'文本1.txt'
    with open(path, 'r+', encoding='utf-8') as f:
        address_list = f.readlines()
    f.close()
    for c in address_list:
        c = c.replace('\n', '')
        c = c.split(',')
        location = Geocoder.get_location(c[0])
        print('{0},{1},{2},{3}'.format(location[3],c[0],location[0],location[1]))
        # print(location[0], location[1],location[3])


if __name__ == '__main__':
    main()
