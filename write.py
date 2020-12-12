import base64
import  os
import json
import socket
import requests
 
# 首先将图片读入
# 由于要发送json，所以需要对byte进行str解码
def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str
 
path = os.getcwd()
print(path)


# 这改成你的图片的路径
img_str_1 = getByte('C:/Users/void/desktop/3.jpg')
img_str_2 = getByte('C:/Users/void/desktop/2.jpg')
# 此时可以测试解码得到图像并显示，服务器端也按照下面的方法还原图像继续进一步处理  
img_decode_1 = img_str_1.encode('ascii')  # ascii编码
img_decode_1_ = base64.b64decode(img_decode_1)  # base64解码

print(img_decode_1_)


def getIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('127.0.0.1', 5000))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# canteen 表示几食堂
canteen = '1' 
data = {'window_1':img_str_1,'window_2':img_str_2, 'type':'0', 'useAntiSpoofing':'0','canteen':canteen}
json_mod = json.dumps(data)
res_pic = requests.post(url = 'http://119.3.181.37:80/app/getPicture', data=json_mod, headers={'Content-Type':'application/json'})



print(res_pic.text)

