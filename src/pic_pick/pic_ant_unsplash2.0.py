# -*- coding:utf-8 -*-
# Usage: fetch pictures from Unsplash
# 1. create a local save_dir = './downloaded_photos/'
# 2. change the collection if of your target website: /collections/1065976/
# Version changelog:
# 1.0: static parsing html tags to locate download urls
# 2.0: dynamic parsing html responded text with json to get picture id, and spliced which into download urls

import requests
import json
import time
import os
import sys
from urllib.request import urlretrieve


class DownloadPhotos(object):
    """docstring for Downloaded_photos"""

    def __init__(self, request_url, order_headers):
        super(DownloadPhotos, self).__init__()
        self.target_site = request_url
        self.headers = order_headers
        self.photo_dict = {}

    def get_photo_urls(self):
        req = requests.get(url=self.target_site, headers=self.headers)
        html = json.loads(req.text)
        for dict in html:
            picid = dict["id"]
            full_url = dict['urls']['full']
            self.photo_dict[picid] = full_url

        return self.photo_dict


if __name__ == '__main__':
    save_dir = './downloaded_photos/'
    order_page_quantity = 6  # download 50 pieces
    order_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'authority': 'unsplash.com',
    }

    print('Start downloading at: ' + time.strftime("%Y/%m/%d %H:%M:%S"))
    for page in range(1, order_page_quantity):
        request_url = "https://unsplash.com/napi/collections/1065976/photos?page=" + \
            str(page) + "&per_page=10&order_by=latest&share_key=17f2f615cdf7ef984bd41f402884e311"
        dlp = DownloadPhotos(request_url, order_headers)
        # print(dlp.get_photo_urls())
        for key, value in dlp.get_photo_urls().items():
            try:
                print('Saving photo: {}'.format(key))
                urlretrieve(value, save_dir + key + '.jpg')
            except NameError:
                print('Failed downloading...')
            except FileNotFoundError:
                os.mkdir(save_dir, mode=0o777)

    print('Completely downloaded all photos to {} at {}'.format(
        save_dir, time.strftime("%Y/%m/%d %H:%M:%S")))
