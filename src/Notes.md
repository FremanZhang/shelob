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

