# -*- coding:utf-8 -*-
# Usage: fetch pictures from Unsplash: https://unsplash.com/t/animals
# 1. create a local folder: "./downloaded_photos/"
# 2. change the target website to your desired: target = 'https://unsplash.com/t/animals'
# Version changelog:
# 1.0: static parsing htm tags to locate download urls

from bs4 import BeautifulSoup
import requests
import sys
# import lxml

from urllib.request import urlretrieve


class DownloadPhotos(object):
    """
    docstring for DownloadPhotos
    incoming args: target-site
    """

    def __init__(self, target_site, headers):
        super(DownloadPhotos, self).__init__()
        self.target_site = target_site
        self.headers = headers
        self.photos_qty = 0
        self.photo_dict = {}

    def get_photo_links(self):
        """
        //*[@id="app"]/div/div[6]/div[2]/div[1]/div/figure[1]/div/div[2]/div[2]/a
        <a title="Download photo" href="https://unsplash.com/photos/lckTrojViao/download?force=true" rel="nofollow" download="" target="_blank" class="_37zTg _1l4Hh _1CBrG _1zIyn xLon9 _1Tfeo NDx0k _2Xklx">
            <svg class="Apljk _11dQc" version="1.1" viewBox="0 0 32 32" width="32" height="32" aria-hidden="false">
                <path d="M25.8 15.5l-7.8 7.2v-20.7h-4v20.7l-7.8-7.2-2.7 3 12.5 11.4 12.5-11.4z">
                </path>
            </svg>
        </a>
        """
        req = requests.get(self.target_site, self.headers)
        html = req.text
        bfs = BeautifulSoup(html, 'lxml')
        # static parsing html tags
        download_hrefs = bfs.find_all('div', id="app")[0].find_all(
            'a', title="Download photo")    

        photos_qty = len(download_hrefs)

        for i in range(photos_qty):
            photo_key = download_hrefs[i].get('title') + str(i)
            self.photo_dict[photo_key] = download_hrefs[i].get('href')

        return self.photo_dict


if __name__ == '__main__':
    target = 'https://unsplash.com/t/animals'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'authority': 'unsplash.com',
        'referer': 'https://unsplash.com/t/animals',
        'path': '/napi/collections/3330452/photos?page=5&per_page=10&order_by=latest&share_key=17f2f615cdf7ef984bd41f402884e311',
        'viewport-width': '485'
    }
    dlp = DownloadPhotos(target, headers)

    pictures = dlp.get_photo_links()
    # print(pictures)
    for key, value in pictures.items():
        print('=================' + key + '=================')
        print(value)
        try:
            urlretrieve(value, './downloaded_photos/' + key + '.jpg')
        except NameError:
            print('Failed downloading...')

        print('Completed downloading!!!')
