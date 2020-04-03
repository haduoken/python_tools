import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np
import base64, json
from xml.etree import ElementTree

# url = 'http://172.16.1.142:80/ISAPI/System/status'
url = 'http://172.16.1.142:80/ISAPI/Security/userCheck'

ptz_status = 'http://172.16.1.142:80/ISAPI/PTZCtrl/channels/1/status'
focus_status = 'http://172.16.1.142:80/ISAPI/Image/channels/1/focusConfiguration'
# focus_status = 'http://172.16.1.142:80/ISAPI/Image/channels/1'
snap_shoot = 'http://172.16.1.142:80/ISAPI/Streaming/channels/1/picture'
snap_shoot_cap = 'http://172.16.1.142:80/ISAPI/Streaming/channels/1/picture/capabilities'

ptz_ex = 'http://172.16.1.142:80/ISAPI/PTZCtrl/channels/1/absoluteEx'
# thermal_cap = 'http://172.16.1.142:80/ISAPI/Thermal/channels/2/thermometry/PixelToPixelParam'
thermal_cap = 'http://172.16.1.142:80/ISAPI/Thermal/channels/2/thermometry/jpegPicWithAppendData?format=json'

# 172.16.1.142
# BQAAAKQUN4H0j6z15gM=
# debug
# BQAAAKQUN4H0j5ap4iA=


preset = 'http://172.16.1.142:80/ISAPI/PTZCtrl/channels/1/presets/500'
preset_data = {
    'enabled': True,
    'id': '500',
    'presetName': '500',
    
}
preset_xml_data = '<PTZPreset xmlns: "http://www.isapi.org/ver20/XMLSchema" version="2.0"> <id>500</id> <presetName>预置点 500 </presetName> </PTZPreset>'
preset_xml_data = preset_xml_data.encode('utf-8')
headers = {
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type': 'application/xml; charset=UTF-8 ',
    # 'jpegPicEnabled': 'True'
    # 'Authorization': 'Digest YWRtaW46a2lsb3gxMjM0'
    # 'WWW-Authenticate': 'Basic realm="admin", charset="UTF-8"'
}

focus_body = {
    # 'focusStyle': 'MANUAL',
    # 'focusPosition': 10,
    # 'focusSpeed': 10,
}
auth = HTTPDigestAuth('admin', 'kilox1234')

# xml = """<?xml version="1.0" encoding="UTF-8"?> <PTZAbsoluteEx version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema"> <elevation>10.000</elevation> </PTZAbsoluteEx>"""
# r = requests.get(url, auth=auth, headers=headers, timeout=30)
# r = requests.get(snap_shoot, auth=auth)
ElementTree.register_namespace('', 'http://www.hikvision.com/ver20/XMLSchema')

# root = ElementTree.fromstring(r.content)

# print(tree)
# a = tree.getroot()
# for child in root:
#     # elevation =
#     print(child.tag)
#     print(child.text)
#     print(child.attrib)


# print(ElementTree.dump(root))

# a = ElementTree.SubElement(tree,'PTZAbsoluteEx')
# elevation = ElementTree.SubElement(a,'elevation')
# print(elevation.text)
# print(elevation.tag)
# print(elevation.attrib)

# a = r.json()
# a = r.content.decode('utf-8',errors='ignore')
# # a = str(r.content)
# data = json.loads(a)
# print(a)

# print(r)

# 1334680
# 1310720,
#
# 199 + 23448 + 1310720 + 23448
# b'--boundary\r\nContent-Type: application/json; charset="UTF-8"\r\nContent-Length: 199\r\n\r\n{\n\t"JpegPictureWithAppendData":\t{\n\t\t"cha' \
# b'nnel":\t2,\n\t\t"jpegPicLen":\t23448,\n\t\t"jpegPicWidth":\t640,\n\t\t"jpegPicHeight":\t512,\n\t\t"p2pDataLen":\t1310720,\n\t\t"isFreezedata":\t' \
# b'0,\n\t\t"temperatureDataLength":\t4\n\t}\n}\r\n--boundary\r\nContent-Disposition: form-data;\r\nContent-Type: image/pjpeg\r\nContent-Length: 23448\
r = requests.get(thermal_cap, auth=auth, headers=headers)

# a = json.loads(r.text.replace("'",'"'))
back = len('\r\n--boundary--\r\n')
content_length = 1310720

raw_jpg = r.content[-(content_length + back):-back]
a = len(raw_jpg)
# print(len(raw_jpg))
# \xa5\xcfAE\x80\xceA\x13\xbd\xcdA'
a = r.text
# print(a)


# print(len(r.content))
# a = r.content
# json.loads()


# xml = """<?xml version='1.0' encoding='utf-8'?>
# <a>б</a>"""


def decode_image(data_bytes):
    # r = requests.put()
    # r = requests.put(preset, auth=auth, headers=headers)init_dis_map
    # print(r)
    data = np.fromstring(data_bytes, np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img


def decode_thermal(data_bytes):
    thermal = np.fromstring(data_bytes, np.float)
    thermal = cv2.imdecode(thermal, cv2.IMREAD_COLOR)
    # thermal_to_show = np.array(thermal, dtype=np.uint8)
    
    thermal_to_show = np.reshape(thermal, [512, 640])
    thermal_to_show[thermal_to_show > 100] = 100
    thermal_to_show[thermal_to_show < 0] = 0
    thermal_to_show *= 2
    thermal_to_show = cv2.applyColorMap(thermal_to_show, cv2.COLORMAP_JET)
    return thermal_to_show

# print(len(data))
# # print(data)
# # print(r.content)
# # print(type(r.content))
# # print(r.content)
# # img_bytes = r.content
# # out = None
# #
# #
# # # image = r.content.decode('utf-8')
# # base64.decode(image, out)
# #
# #
# # image = np.asarray(r.content, dtype="uint8")
# # print(image)
# # print(out)
# img = decode_thermal(r.content)
# cv2.imshow('window', img)
# cv2.waitKey(0)
# cv2.imwrite('isapi.png', img)
