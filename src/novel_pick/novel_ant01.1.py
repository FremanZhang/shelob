# -*- coding:utf-8 -*-
# Usage: fetch novel from http://www.biqukan.com/
from bs4 import BeautifulSoup
import requests
import sys


# 网页抓取，html信息初始化
def prepare_webpage(page_url):
    req = requests.get(url=page_url)
    html = req.text
    bfs = BeautifulSoup(html, features="html.parser")
    return bfs

# 下载器类


class Downloader(object):

    def __init__(self):
        self.site_url = 'https://www.biqukan.com'    # 目标站点url
        self.target_novel_url = 'https://www.biqukan.com/1_1408/'    # 目标小说url
        self.chapter_names = []    # 存放章节信息
        self.chapter_urls = []    # 章节链接
        self.nums = 0    # 章节数

    # 章节信息解析--名称，网址链接
    def get_chapters(self):
        chapter_bf = prepare_webpage(self.target_novel_url)  # 目录页bfs初始化
        chapter_div = chapter_bf.find_all('div', class_='listmain')
        a_tags = chapter_div[0].find_all('a')   # 章节超链接
        self.nums = len(a_tags[12:])
        for a in a_tags[12:]:
            self.chapter_names.append(a.string)
            self.chapter_urls.append(self.site_url + a.get('href'))

    # 章节详细内容解析
    def get_chapter_contents(self, chapter_content_url):
        content_bf = prepare_webpage(chapter_content_url)
        texts = content_bf.find_all('div', class_='showtxt', id='content')
        try:
            chapter_text = str(texts[0].text.replace('\xa0' * 8, '\n\n'))
            return chapter_text
        except IndexError:
            print(chapter_content_url)

    # 内容写入本地文件
    def write_to_local(self, chapter_name, path, chapter_text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            try:
                f.write(chapter_name + '\n')
                f.writelines(chapter_text)
                f.write('\n\n')
            except TypeError:
                print(chapter_name)


if __name__ == "__main__":
    dl = Downloader()
    dl.get_chapters()
    print('Start downloading:')
    for i in range(dl.nums):
        dl.write_to_local(
            dl.chapter_names[i], './fjwd.txt', dl.get_chapter_contents(dl.chapter_urls[i]))
        sys.stdout.write("Downloading: %.1f%%" % float(i / dl.nums) + '\r')
        sys.stdout.flush()
    print('Completed downloading!!!')
