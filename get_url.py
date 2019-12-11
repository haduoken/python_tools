import requests, json
import pandas  as pd
from tqdm import tqdm
import math
from tes_selenium import TestSelenium


class ExcelProcess:
    def __init__(self):
        self.ts = TestSelenium()
        pass
    
    def process(self, in_out_file):
        df = pd.read_excel(in_out_file)
        
        times = df['签收时间']
        
        valuse = df.ix[:, ['快递公司', '物流单号', '手机号后四位', '签收时间']].values
        
        current_cnt = 0
        for index, data in enumerate(tqdm(valuse)):
            company, tracking_number, phone_number, receive_time = data
            tracking_number = str(tracking_number)
            tracking_number = tracking_number.strip('\t')
            phone_number = str(phone_number)
            
            ok = False
            if isinstance(receive_time, float):
                if math.isnan(receive_time):
                    time = ''
                    if company != '顺丰标准到付' and company != '顺丰标准快递' and company != '顺丰国际':
                        ok, time = self.ts.get_tracking_num_SF_100(tracking_number, phone_number)
                    if company == 'FedEx':
                        ok, time = self.ts.get_tracking_num_DHL(tracking_number)
                    if company == 'DHL国际快递':
                        ok, time = self.ts.get_tracking_num_DHL(tracking_number)
                    
                    if ok:
                        times[index] = time
                        current_cnt += 1
            if current_cnt >= 10:
                df.to_excel(in_out_file, index=False, header=True)
                current_cnt = 0
                print('************* 保存一次 *************')
        df.to_excel(in_out_file, index=False, header=True)


if __name__ == "__main__":
    ep = ExcelProcess()
    ep.process('result.xlsx')
    pass
