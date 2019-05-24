# -*- coding: utf-8 -*-
# Usage: Produce and share traffic situation photo by wechat daily
# 0.1 - Capture navigation .png screenshot through Selenium
# 0.2 - Send pic and traffic status to wechat friend
# 0.3 - Running multiple wechat instances in backend for different jobs
# 0.4 - Integrated amap APIs of weather, RT traffic, circle, info-window and Wechat


import json
import os
import time
import re

import itchat
import requests
import schedule
from urllib import request
from selenium import webdriver


def save_to_log(string):
    f_log = open('running_log.log', 'a')
    f_log.write(string + "\n")
    f_log.close()


class Location(object):
    def __init__(self, headers, key, address, city, province):
        self.headers = headers
        self.key = key
        self.address = address
        self.city = city
        self.province = province
        self.location_geoXY = {}
        self.restapi = 'http://restapi.amap.com/v3/geocode/geo?key=' + \
            self.key + '&address=' + self.address + '&city=' + self.city['cn']

    def get_lgeoXY(self):
        req = requests.get(url=self.restapi, headers=self.headers)
        html = json.loads(req.text)
        self.location_geoXY = html
        return self.location_geoXY

    def get_moji_weather(self):
        url = "https://tianqi.moji.com/weather/china/%s/%s" % (
            self.province, self.city['en'])
        par = '(<meta name="description" content=")(.*?)(">)'
        html = request.urlopen(url).read().decode("utf-8")
        data = re.search(par, html).group(2)
        # print(data)
        return data


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
        req = requests.get(url=self.restapi, headers=self.headers)
        html = json.loads(req.text)
        self.traffic_info = html
        return self.traffic_info

    def get_navigationPic(self, navPic, amapTempalte):

        global driver
        try:
            driver = webdriver.Chrome()
            driver.set_page_load_timeout(30)
            driver.get(
                "file://%s" % amapTempalte)
            time.sleep(7)
            driver.maximize_window()
            time.sleep(3)
            # this will overwrite the file with the same name
            driver.save_screenshot(navPic)
            save_to_log('Screenshot %s to %s done!' % (amapTempalte, navPic))
            driver.quit()
        except TimeoutError:
            save_to_log('Chrome web page responded timeout.')
            driver.quit()
        except IOError:
            save_to_log('Failed screenshot!')
            driver.quit()


class Wechat(object):
    def __init__(self):
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        save_to_log('Wechat login successfully.')

    def sendPersonalMsg(self, msg, personName=None):
        # 使用备注名来查找实际用户名
        users = itchat.search_friends(name=personName)
        # 获取好友全部信息,返回一个列表,列表内是一个字典
        # 获取`UserName`,用于发送消息
        userName = users[0]['UserName']
        # print(userName)
        save_to_log('Sending meesage:\n %s' % msg)
        itchat.send(msg, toUserName=userName)
        save_to_log('Sent message to {} successfully'.format(
            users[0]['NickName']))

    def sendGroupMsg(self, msg, roomNames=None):
        # roomNames is a alias list of the target groups
        itchat.get_chatrooms(update=True)
        for roomName in roomNames:
            save_to_log(roomName)
            iRoom = itchat.search_chatrooms(roomName)
            # save_to_log(iRoom)
            for room in iRoom:
                save_to_log(room['UserName'])
                itchat.send(msg, room['UserName'])


# Scheduling job
def job():

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    baseDir = os.path.dirname(os.path.abspath('__file__'))

    # Variables for Amap
    ws_key = 'xxxxxxxxxxxxxxxxxx'
    address = 'xxxxxxxxxx'
    city = {'cn': '中文城市名', 'en': 'city EN name'}
    province = 'Guangdong'
    radius = '5000'
    navPic = baseDir + '/navPic' + time.strftime("%Y%m%d") + '.png'
    amapTempalteSrc = baseDir + '/template_rt_weather_circle_info_src.html'     # 原始模板
    amapTempalte = baseDir + "/template_rt_weather_circle_info.html"            # 整合信息后供正式抓取的临时模板

    # Variables for wechat
    wxFriend = 'xxxxxx'
    wxGroups = ['xxxxx', 'xxxxxxxxxxxxxx']

    save_to_log("================= Starting job at %s =================" %
                time.strftime("%Y/%m/%d %H:%M:%S"))
    # Parse coordination for the given address
    location = Location(headers=headers, key=ws_key,
                        address=address, city=city, province=province)
    locationCoord = location.get_lgeoXY()['geocodes'][0]['location']

    # Query the traffic information of specified radius circle area
    trafficInfo = Traffic(headers=headers, key=ws_key,
                          coord=locationCoord, radius=radius)

    summary = "{}市{}方圆{}米内综合交通态势为: {}<br>".format(city['cn'], address, radius, trafficInfo.get_traffic_info()[
        'trafficinfo']['evaluation']['description'])
    detail = "详细路况： {}<br>".format(trafficInfo.get_traffic_info()[
                                     'trafficinfo']['description'])
    # Replace placeholder string with realtime traffic status information
    f = open(amapTempalteSrc, 'r')
    lines = f.readlines()
    f.close()
    f = open(amapTempalte, "w+")
    for line in lines:
        a = re.sub('Content4PicPlaceholder', summary + detail, line)
        f.writelines(a)
    f.close()

    # Best navigation route, return as a screenshot picture
    trafficInfo.get_navigationPic(navPic, amapTempalte)
    os.remove(amapTempalte)     # 使用完删除

    # Execute Wechat sending tasks
    wechatJob = Wechat()
    textMsg = "{}\n\n{}\n{}\n\n未来详细天气预报及实时路况，请点击下面图片中[查看原图]了解详情".format(location.get_moji_weather(), summary, detail)
    wechatJob.sendPersonalMsg(msg=textMsg, personName=wxFriend)
    wechatJob.sendGroupMsg(msg=textMsg, roomNames=wxGroups)
    picMsg = "@img@%s" % navPic
    wechatJob.sendPersonalMsg(msg=picMsg, personName=wxFriend)
    wechatJob.sendGroupMsg(msg=picMsg, roomNames=wxGroups)
    save_to_log("================= Job completed at %s ================" %
                time.strftime("%Y/%m/%d %H:%M:%S"))


if __name__ == '__main__':

    # job()
    schedule.every().day.at("18:00").do(job)    # 下班
    schedule.every().day.at("07:10").do(job)    # 上班
    while True:
        schedule.run_pending()
        time.sleep(1)
