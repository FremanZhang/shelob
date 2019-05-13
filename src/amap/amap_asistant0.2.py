# -*- coding: utf-8 -*-
# Usage: Produce and share traffic situation photo by wechat daily
# 1. Screenshot navigation .png through Selenium
# 2. Watermark the picture above with rtRoadStatus text


import requests
import json
import time
import itchat
import os
from selenium import webdriver


class Location(object):

    def __init__(self, headers, key, address, city):
        self.headers = headers
        self.key = key
        self.address = address
        self.city = city
        self.location_geoXY = {}
        self.restapi = 'http://restapi.amap.com/v3/geocode/geo?key=' + \
            self.key + '&address=' + self.address + '&city=' + self.city

    def get_lgeoXY(self):
        req = requests.get(url=self.restapi, headers=self.headers)
        html = json.loads(req.text)
        self.location_geoXY = html

        return self.location_geoXY


class Traffic(object):
    def __init__(self, headers, key, coord, radius):
        self.headers = headers
        self.key = key
        self.coord = coord
        self.radius = radius
        self.traffic_info = {}
        self.restapi = 'http://restapi.amap.com/v3/traffic/status/circle?key=' + self.key + \
            '&location=' + self.coord + '&radius=' + self.radius + '&level6&extensions=all'

    def get_traffic_info(self):
        req = requests.get(url=self.restapi, headers=headers)
        html = json.loads(req.text)
        self.traffic_info = html

        return self.traffic_info

    def get_navigationPic(self):

        try:
            driver = webdriver.Chrome()
            driver.get(
                "file://abspath_to_amap_ws_html_doc")
            driver.maximize_window()
            # this will overwrite the file with the same name

            time.sleep(5)
            driver.save_screenshot("./navigationPic.png")
            print('screenshot done')
            driver.quit()

            # dir_path = os.path.dirname(
            #     os.path.abspath('navigationPic.png'))
            # pic_abspath = dir_path + 'navigationPic.png'
        except IOError:
            print('Failed screenshot!')


class Wechat(object):

    def __init__(self):
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        print('Wechat login successfully.')

    def sendPersonalMsg(self, msg, personName=None):
        users = itchat.search_friends(name=personName)
        userName = users[0]['UserName']
        itchat.send(msg, toUserName=userName)
        print('Sent message to {} successfully'.format(users[0]['NickName']))

    def sendGroupMsg(self, msg, roomNames=None):
        # roomNames is a alias list of the target groups
        itchat.get_chatrooms(update=True)
        for roomName in roomNames:
            print(roomName)
            iRoom = itchat.search_chatrooms(roomName)
            print(iRoom)
            for room in iRoom:
                print(room['UserName'])
                itchat.send_msg(msg, room['UserName'])


if __name__ == '__main__':
    ws_key = 'xxxxxxxxxxxxxxxxxxxxxx'  # amap web service key
    address = 'xxxxx'   # location name
    city = 'xx'     # city name
    radius = '3000'

    # param for wechat
    personName = 'xxxx'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    location = Location(headers=headers, key=ws_key,
                        address=address, city=city)
    locationCoord = location.get_lgeoXY()['geocodes'][0]['location']
    trafficInfo = Traffic(headers=headers, key=ws_key,
                          coord=locationCoord, radius=radius)

    summary = "{}市{}方圆{}米内综合交通态势为: {}" .format(city, address, radius, trafficInfo.get_traffic_info()[
        'trafficinfo']['evaluation']['description'])
    detail = "详细道路信息： {}" .format(trafficInfo.get_traffic_info()[
        'trafficinfo']['description'])

    print("=============================================================")
    print(summary)
    print("=============================================================")
    print(detail)

    wechatJob = Wechat()
    wechatJob.sendPersonalMsg(msg=(summary + '\n' + detail), personName='渔之乐')

    trafficInfo.get_navigationPic()
    picMsg = "@img@%s" % 'abspath_to_pic'
    wechatJob.sendPersonalMsg(msg=picMsg, personName=personName)
