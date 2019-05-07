# Usage:

    sudo apt install -y python3-pip
    sudo apt install build-essential libssl-dev libffi-dev python3-dev
    sudo apt install -y python3-venv

    mkdir crawler
    cd crawler/
    python3.6 -m venv venv
    source venv/bin/activate
    
    git clone https://github.com/FremanZhang/shelob.git
    pip install -r shelob/src/requirements.txt
    cd shelob/
    git pull



# Processing logic:

## Picking static texts

1. 使用requeusts获取整个网页的HTML信息；
2. 抓取章节信息（名称，链接，数量）
3. 抓取章节详细内容文本
4. 写入前面2&3步骤采集的内容到本地文件，按章节分隔对应
5. 显示下载进度百分比


## Picking dynamic pictures

### static parsing html tags

1. 处理请求响应头部headers
2. 绕过ssl
3. 统计figures Qty.
4. 依据Qty. 用For range循环解析每个figure，拿到a title="Download photo" 
5. 取得每个a tag的超链url href
6. 用urlretrieve()根据href超链接下载图片（inspect网页发现下载超链接会直接带出来）

    https://images.unsplash.com/photo-1555661059-7e755c1c3c1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjExMDk0fQ&auto=format&fit=crop&w=600&q=60
    https://unsplash.com/photos/lckTrojViao/download?force=true


### dynamic parsing html context as json

1. 组合XHR request_url
2. 透过Response返回信息解析json pattern: [{picid0_dict18}, {picid2_dict18}, …, {picid9_dict18}]
3. 分析json数据拿到图片下载地址:

    >>> req = requests.get(url='https://unsplash.com/napi/collections/3330452/photos?page=1&per_page=10&order_by=latest&share_key=17f2f615cdf7ef984bd41f402884e311')
    >>> for dict in html:
    ...     picid = dict["id"]
    ...     print(picid)
    ... 
    w2d6dMhVHR4
    sirEpWjfSmo
    NicYcQcZ-wE
    pn_TY-8_Pbk
    SkvPuo5jxVM
    wvO5tPfTpug
    iYQC9xWMvw4
    Ynb1v7l3B_0
    LOlMe8HfofI
    A81818EFqGQ

    >>> print(html[0]['urls']['full'])
    https://images.unsplash.com/photo-1491193348662-47874a96c621?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&ixid=eyJhcHBfaWQiOjEyMDd9
    >>> 

4. 用urlretrieve()下载图片