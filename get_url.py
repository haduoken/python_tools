#!/usr/bin/python3
import requests, json
import pandas  as pd
from tqdm import tqdm
import math
from tes_selenium import TestSelenium
from decorator import try_except


class ExcelProcess:
    def __init__(self):
        self.ts = TestSelenium()
        self.current_cnt = None
        self.times = None
        self.target_type = None
        self.df = None
        self.in_out_file = None
        self.skip_type = []
        pass
    
    @try_except
    def process_one(self, index, data):
        company, tracking_number, phone_number, receive_time = data
        tracking_number = str(tracking_number)
        tracking_number = tracking_number.strip('\t')
        phone_number = str(phone_number)
        phone_number = phone_number[-4:]
        
        if self.target_type != '':
            if company != self.target_type:
                return
        if company in self.skip_type:
            return
        
        ok = False
        print('[ExcelProcess]  尝试获取 {}'.format(company))
        if isinstance(receive_time, float):
            if math.isnan(receive_time):
                time = ''
                if company == '顺丰标准到付' or company == '顺丰标准快递' or company == '顺丰国际':
                    ok, time = self.ts.get_tracking_num_SF_100(tracking_number, phone_number)
                if company == 'FedEx':
                    ok, time = self.ts.get_tracking_num_FedEx(tracking_number)
                if company == 'DHL国际快递':
                    ok, time = self.ts.get_tracking_num_DHL(tracking_number)
                if company == '美国UPS' or company == '亚马逊物流':
                    ok, time = self.ts.get_tracking_num_100(tracking_number)
                
                if ok:
                    print('获取到时间', time)
                    self.times[index] = time
                    self.current_cnt += 1
        if self.current_cnt >= 10:
            self.df.to_excel(self.in_out_file, index=False, header=True)
            self.current_cnt = 0
            print('************* 保存一次 *************')
    
    def process(self, in_out_file, skip_type, target_type=''):
        self.df = pd.read_excel(in_out_file)
        self.target_type = target_type
        self.skip_type = skip_type
        
        self.times = self.df['签收时间']
        self.in_out_file = in_out_file
        
        # valuse = df.ix[:, ['快递公司', '物流单号', '手机号后四位', '签收时间']].values
        # valuse = self.df.ix[:, ['物流公司', '物流单号', '收货人电话', '签收时间']].values
        valuse = self.df.ix[:, ['物流公司', '物流单号', '收件人电话', '签收时间']].values
        
        self.current_cnt = 0
        for index, data in enumerate(tqdm(valuse)):
            self.process_one(index, data)
        self.df.to_excel(in_out_file, index=False, header=True)


if __name__ == "__main__":
    ep = ExcelProcess()
    # ep.process('result.xlsx', target_type='FedEx')
    ep.process('线上签收时间.xlsx', ['DHL国际快递'])
    pass
