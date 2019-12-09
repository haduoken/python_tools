import requests, json
import pandas  as pd
from tqdm import tqdm
from tes_selenium import get_tracking_num


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


def parse():
    df = pd.read_excel('2.xlsx', sheet_name='Sheet1')
    # for line in df.iloc[1:10, [1, 10]]:
    #     a = line
    companys = df['物流公司']
    tracking_numbers = df['物流单号']
    times = df['签收时间']

    valuse = df.ix[:, ['物流公司', '物流单号', '签收时间']].values

    current_cnt = 0
    for index, data in enumerate(tqdm(valuse)):
        current_cnt += 1

        company, tracking_number, time = data
        tracking_number = str(tracking_number)
        tracking_number = tracking_number.strip('\t')
        if company == 'DHL国际快递':
            # times[index] = DHL(tracking_number)
            pass
        elif company == '':
            ok, time = get_tracking_num(tracking_number)
            if ok:
                times[index] = time
            # times[index] = get_tracking_num(tracking_number)
        # if company == 'FedEx':
        #     times[index] = FedEx(tracking_number)

        # 每5个保存一次文件
        if current_cnt >= 5:
            df.to_excel('2.xlsx', sheet_name='Sheet2', index=False, header=True)
            current_cnt = 0
            print('保存一次文件 当前已保存', index)


parse()

if __name__ == "__main__":
    # while True:
    #     main()
    #     i = input("是否继续查询?(任意字符为继续,q为退出)")
    #     if i == "q":
    #         print("感谢使用,祝您生活愉快,再见!")
    #         break
    pass
