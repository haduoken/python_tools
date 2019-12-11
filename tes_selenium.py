import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException, \
    WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

chrome_opt = Options()  # 创建参数设置对象.
chrome_opt.add_argument('--headless')  # 无界面化.
chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.


class TestSelenium:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser_current = None
    
    def get_visible_element(self, xpath):
        try:
            closer_btn = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        except:
            return None
        
        return closer_btn
    
    def get_presence_element(self, xpath):
        try:
            closer_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return None
        
        return closer_btn
    
    def get_tracking_num_DHL(self, tracking_number):
        params = {'trackingNumber': str(tracking_number),
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
            print('DHL {} 时间 {}'.format(tracking_number, arrive_time))
        except KeyError:
            return False, 0
        return True, arrive_time
    
    def get_tracking_num_FedEx(self, tracking_number):
        try:
            if self.browser_current != 'https://www.kuaidi100.com/global/fedexus.shtml?from=openv':
                self.browser_current = 'https://www.kuaidi100.com/global/fedexus.shtml?from=openv'
                self.browser.get(self.browser_current)
            input_bar = self.browser.find_element_by_name("postid")
            input_bar.click()
            input_bar.clear()
            input_bar.send_keys(tracking_number)
            
            ensure_btn = self.browser.find_element_by_id('query')
            ensure_btn.click()
            
            date = self.get_visible_element('/html/body/div[3]/div[3]/div[1]/div[6]/table/tbody/tr[1]/td[1]')
            # import time
            # time.sleep(1)
            if date is not None:
                time = date.text
                return True, time
            else:
                print('获取失败')
                return False, 0
        except:
            print('获取失败')
            return False, 0
    
    def get_tracking_num_SF_100(self, tracking_number, phone_number):
        if phone_number.find('*') != -1:
            return False, 0
        if phone_number.find('.') != -1:
            return False, 0
        if phone_number == '':
            return False, 0
        try:
            if self.browser_current != 'https://www.kuaidi100.com':
                self.browser_current = 'https://www.kuaidi100.com'
                self.browser.get('https://www.kuaidi100.com')
            
            check_btn = self.get_visible_element('/html/body/div[7]/div[2]/div/a')
            if check_btn is not None:
                check_btn.click()
            
            input_bar = self.browser.find_element_by_name("postid")
            
            input_bar.click()
            input_bar.clear()
            input_bar.send_keys(tracking_number)
            
            ensure_btn = self.browser.find_element_by_id('query')
            ensure_btn.click()
            
            input = WebDriverWait(self.browser, 2).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="checkCode"]/div[2]/div/div[2]/input[1]'))
            )
            
            ActionChains(self.browser).send_keys_to_element(input, phone_number[0]).perform()
            input = self.browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[2]')
            ActionChains(self.browser).send_keys_to_element(input, phone_number[1]).perform()
            input = self.browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[3]')
            ActionChains(self.browser).send_keys_to_element(input, phone_number[2]).perform()
            input = self.browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[4]')
            ActionChains(self.browser).send_keys_to_element(input, phone_number[3]).perform()
            
            ensure_btn = self.browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[3]')
            ensure_btn.click()
            
            date = WebDriverWait(self.browser, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="queryResult"]/div[3]/div[2]/table/tbody/tr[1]/td[1]'))
            )
            print(date.text)
            return True, date.text
        except (TimeoutException, NoSuchElementException, ElementNotVisibleException, WebDriverException, TypeError):
            print('无法获取')
            return False, 0
