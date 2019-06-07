import requests

def robot(info):
    #info = msg['Content'].encode('utf8')
    # 图灵API接口
    api_url = 'http://openapi.tuling123.com/openapi/api/v2'
    # 接口请求数据
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": str(info)
            }
        },
        "userInfo": {
            "apiKey": "fa58083cc686409788e27a2888399b71",
            "userId": "457871"
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Host': 'openapi.tuling123.com',
        'User-Agent': 'Mozilla/5.0 (Wi`ndows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 '
                      'Safari/537.36 '
    }
    # 请求接口
    result = requests.post(api_url, headers=headers, json=data).json()
    # 提取text，发送给发信息的人
    return result['results'][0]['values']['text']

print(robot("你好"))