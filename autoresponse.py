import itchat
import datetime
import requests
import city_dict

global t, name, rtext
t = 0

#输入自动回复对象的微信备注名称，一次仅能一人
print("请输入要自动回复对象的备注名（一个对象）：")
name = input()

#输入自动回复的内容
print("请输入自动回复内容：")
rtext = input()

#获取日期信息
nowdate = datetime.datetime.now().strftime('%Y-%m-%d %A')

def isJson(resp):
    try:
        resp.json()
        return True
    except:
        return False

#获取天气信息
def get_weather_info(city_code):
    weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'
    resp = requests.get(url=weather_url)
    if resp.status_code == 200 and isJson(resp) and resp.json().get('status') == 200:
        weatherJson = resp.json()
        # 今日天气
        today_weather = weatherJson.get('data').get('forecast')[1]
        # 温度
        high = today_weather.get('high')
        high_c = high[high.find(' ') + 1:]
        low = today_weather.get('low')
        low_c = low[low.find(' ') + 1:]
        temperature = f"温度 : {low_c}/{high_c}"
        # 空气指数
        aqi = today_weather.get('aqi')
        aqi = f"空气质量 : {aqi}"
        # 天气
        tianqi = today_weather.get('type')
        tianqi = f"天气 : {tianqi}"

        today_msg = f'{tianqi}\n{temperature}\n{aqi}\n'
        return today_msg

#图灵机器人接口
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

#自动回复程序
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE])
def reply_msg(msg):
    global t, name, rtext
    userName = msg['User']['UserName']
    if t == 2:
        if msg['User']['RemarkName'] == name:
            if msg['Content'] == "退出":
                itchat.send("机器人已退出", toUserName=userName)
                t = 0
            else:
                text = msg['Content']
                rep = robot(text)
                itchat.send(rep+"\n回复“退出”，退出机器人聊天", toUserName=userName)
    elif t == 1:
        if msg['User']['RemarkName'] == name:
            ctn = msg['Content']
            if ctn in city_dict.city_dict:
                city_code = city_dict.city_dict[ctn]
                wheather = get_weather_info(city_code)
                itchat.send(wheather, toUserName=userName)
            else:
                itchat.send("无法获取您输入的城市信息", toUserName=userName)
        t = 0
    else:
        if msg['User']['RemarkName'] == name:
            if msg['Content'] == '你好':
                itchat.send('你好', toUserName=userName)
            elif msg['Content'] == '天气':
                itchat.send('请输入您要查询的城市名', toUserName=userName)
                t = 1
            elif msg['Content'] == '日期':
                itchat.send(nowdate, toUserName=userName)
            elif msg['Content'] == '聊天':
                itchat.send('你好，我是人工智障', toUserName=userName)
                t = 2
            else:
                itchat.send(rtext + '，自动消息\n回复“日期”，获取日期\n回复“天气”，获取天气\n回复“聊天”，开始和机器人聊天', toUserName=userName)

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
