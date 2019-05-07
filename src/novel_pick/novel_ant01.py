# -*- coding:utf-8 -*-
# Usage: fetch novel from http://www.biqukan.com/
import requests
from bs4 import BeautifulSoup


def get_html_bfs(target):
    req = requests.get(target)
    html = req.text
    bfs = BeautifulSoup(html)
    return bfs


if __name__ == '__main__':
    site = 'https://www.biqukan.com'
    content_target = 'https://www.biqukan.com/0_159/20531521.html'
    content_texts = get_html_bfs(
        content_target).find_all('div', class_='showtxt')
    print(content_texts[0].text.replace('\xa0' * 8, '\n\n'))

    chapter_target = 'https://www.biqukan.com/0_159/'
    chapter_texts = get_html_bfs(
        chapter_target).find_all('div', class_='listmain')
    chapter_texts_hrefs = chapter_texts[0].find_all('a')
    for a in chapter_texts_hrefs:
        print(a.string, site + a.get('href'))
