import os
os.makedirs('./image/', exist_ok=True)
IMAGE_URL = "http://image.nationalgeographic.com.cn/2017/1122/20171122113404332.jpg"


def urllib_download():
    from urllib.request import urlretrieve
    urlretrieve(IMAGE_URL, './image/img1.png')


def request_download():
    import requests
    r = requests.get(IMAGE_URL)
    with open('./image/img2.png', 'wb') as f:
        f.write(r.content)


def chunk_download():
    import requests
    r = requests.get(IMAGE_URL, stream=True)
    with open('./image/img3.png', 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)


urllib_download()
print('download img1')
request_download()
print('download img2')
chunk_download()
print('download img3')
