import requests, json
import pandas  as pd
from tqdm import tqdm
import math
from tes_selenium import get_tracking_num, get_tracking_num_SF_100


def DHL(trackingNumber):
    params = {'trackingNumber': str(trackingNumber),
              'language': 'zh',
              'requesterCountryCode': 'CN'
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

    }
    url = 'https://www.logistics.dhl/utapi'

    try:
        r = requests.get(url, params=params, headers=headers).json()

        arrive_time = r['shipments'][0]['status']['timestamp']
        print('DHL {} 时间 {}'.format(trackingNumber, arrive_time))
    except KeyError:
        return 0
    return arrive_time


def FedEx(trackingNumber='129335520272'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

    }
    url = 'https://www.fedex.com/trackingCal/track'
    data = json.loads(
        '{"TrackPackagesRequest":{"appType":"WTRK","appDeviceType":"","supportHTML":true,"supportCurrentLocation":true,"uniqueKey":"","processingParameters":{},"trackingInfoList":[{"trackNumberInfo":{"trackingNumber":"129335520272","trackingQualifier":"","trackingCarrier":""}}]}}')
    data['TrackPackagesRequest']['trackingInfoList'][0]['trackNumberInfo']['trackingNumber'] = trackingNumber
    params = {'data': data, 'action': 'trackpackages', 'locale': 'zh_CN', 'version': 1, 'format': 'json'}
    r = requests.post(url, params=params, headers=headers).json()
    # a = r
    try:
        arrive_time = r['TrackPackagesResponse']['packageList'][0]['displayActDeliveryDateTime']
        print('FedEx {} 时间 {}'.format(trackingNumber, arrive_time))
    except KeyError:
        return 0
    return arrive_time


# FedEx()


def Express100(trackingNumber='129335520272'):
    params = {'postid': str(trackingNumber),
              # 'language': 'zh',
              # 'requesterCountryCode': 'CN'
              'type': 'fedex',
              'id': 4,
              'valicode': '',
              'tmp': 0.7895764382626502,
              'temp': 0.08769087120054486,
              'platform': 'MWWW'
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'https://www.kuaidi100.com/frame/bing/?iframeId=2699975952',
        'Host': 'www.kuaidi100.com'
        # 'Cookie': 'csrftoken=eEbp5_bqpIQegUaMY66y8dgKTu7Vjz5O5HNRm_lOGbo; WWWID=WWW6977E6C32CACDFEF8EF96C786895B39B; Hm_lvt_22ea01af58ba2be0fec7c11b25e88e6c=1575766316; Hm_lpvt_22ea01af58ba2be0fec7c11b25e88e6c=1575766316; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1'
    }
    # url = 'https://www.kuaidi100.com/query'
    url = 'https://m.kuaidi100.com/query'
    try:
        r = requests.get(url, params=params, headers=headers).json()

        a = r
        arrive_time = r['shipments'][0]['status']['timestamp']
        print('DHL {} 时间 {}'.format(trackingNumber, arrive_time))
    except KeyError:
        return 0
    return arrive_time


# Express100()

# 527233538612869650	顺丰标准到付	"235609499749	"	18503089505	9505
def parseDHL():
    df = pd.read_excel('out.xlsx')

    times = df['签收时间']

    valuse = df.ix[:, ['快递公司', '物流单号', '手机号后四位', '签收时间']].values

    current_cnt = 0
    for index, data in enumerate(tqdm(valuse)):
        current_cnt += 1

        company, tracking_number, phone_number, receive_time = data
        tracking_number = str(tracking_number)
        tracking_number = tracking_number.strip('\t')

        if company != 'DHL国际快递':
            continue

        elif isinstance(receive_time, float):
            if math.isnan(receive_time):
                time = DHL(tracking_number)
                times[index] = time
            # print('phone number is ', phone_number)

            # times[index] = get_tracking_num(tracking_number)
        # if company == 'FedEx':
        #     times[index] = FedEx(tracking_number)

        # 每5个保存一次文件
    df.to_excel('out1.xlsx', sheet_name='Sheet2', index=False, header=True)


def parse2():
    df = pd.read_excel('out1.xlsx')

    times = df['签收时间']

    valuse = df.ix[:, ['快递公司', '物流单号', '手机号后四位', '签收时间']].values

    current_cnt = 0
    for index, data in enumerate(tqdm(valuse)):
        current_cnt += 1
        if index < 4362:
            continue

        company, tracking_number, phone_number, receive_time = data
        tracking_number = str(tracking_number)
        tracking_number = tracking_number.strip('\t')

        if company != '顺丰标准到付' and company != '顺丰标准快递' and company != '顺丰国际':
            continue

        elif isinstance(receive_time, float):
            if math.isnan(receive_time):
                ok, time = get_tracking_num_SF_100(tracking_number, str(phone_number))
                if ok:
                    times[index] = time
            # print('phone number is ', phone_number)

            # times[index] = get_tracking_num(tracking_number)
        # if company == 'FedEx':
        #     times[index] = FedEx(tracking_number)

        # 每5个保存一次文件
        if current_cnt >= 10:
            df.to_excel('out2.xlsx', sheet_name='Sheet2', index=False, header=True)
            current_cnt = 0
            print('保存一次文件 当前已保存', index)
    df.to_excel('out2.xlsx', sheet_name='Sheet2', index=False, header=True)

    # 销售单号
    # 快递公司
    # 物流单号
    # 收货人手机
    # 手机号后四位
    # 签收时间
    # 网址


parse2()

if __name__ == "__main__":
    # while True:
    #     main()
    #     i = input("是否继续查询?(任意字符为继续,q为退出)")
    #     if i == "q":
    #         print("感谢使用,祝您生活愉快,再见!")
    #         break
    pass
