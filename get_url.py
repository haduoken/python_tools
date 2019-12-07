import requests, json
import pandas  as pd


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


def FedEx(trackingNumber):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        
    }
    url = 'https://www.fedex.com/trackingCal/track'
    data = json.loads(
        '{"TrackPackagesRequest":{"appType":"WTRK","appDeviceType":"","supportHTML":true,"supportCurrentLocation":true,"uniqueKey":"","processingParameters":{},"trackingInfoList":[{"trackNumberInfo":{"trackingNumber":"129335520272","trackingQualifier":"","trackingCarrier":""}}]}}')
    data['TrackPackagesRequest']['trackingInfoList'][0]['trackNumberInfo']['trackingNumber'] = trackingNumber
    params = {'data': data, 'action': 'trackpackages'}
    r = requests.post(url, params=params, headers=headers).json()
    # a = r
    try:
        arrive_time = r['TrackPackagesResponse']['packageList'][0]['displayActDeliveryDateTime']
        print('FedEx {} 时间 {}'.format(trackingNumber, arrive_time))
    except KeyError:
        return 0
    return arrive_time


def parse():
    df = pd.read_excel('/home/kilox/Downloads/2.xlsx', sheet_name='Sheet1')
    # for line in df.iloc[1:10, [1, 10]]:
    #     a = line
    companys = df['物流公司']
    tracking_numbers = df['物流单号']
    times = df['签收时间']
    
    valuse = df.ix[:, ['物流公司', '物流单号', '签收时间']].values
    
    for index, data in enumerate(valuse):
        company, tracking_number, time = data
        tracking_number = str(tracking_number)
        tracking_number = tracking_number.strip('\t')
        if company == 'DHL国际快递':
            # times[index] = DHL(tracking_number)
            pass
        if company == 'FedEx':
            times[index] = FedEx(tracking_number)
    
    df.to_excel('2.xlsx', sheet_name='Sheet2', index=False, header=True)


parse()

if __name__ == "__main__":
    # while True:
    #     main()
    #     i = input("是否继续查询?(任意字符为继续,q为退出)")
    #     if i == "q":
    #         print("感谢使用,祝您生活愉快,再见!")
    #         break
    pass
