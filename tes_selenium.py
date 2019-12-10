from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException, \
    WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# from selenium.web
# chrome = webdriver.Chrome()

chrome_opt = Options()  # 创建参数设置对象.
chrome_opt.add_argument('--headless')  # 无界面化.
chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.

# 创建Chrome对象并传入设置信息.
# browser = webdriver.Chrome(chrome_options=chrome_opt)
browser = webdriver.Chrome()

browser.get('https://www.kuaidi100.com')
# browser.get('file:///home/kilox/Downloads/test.html')
# browser.get('http://www.kuaidiwo.cn/shunfeng.html')
input_bar = browser.find_element_by_name("postid")


# browser.get('https://www.sf-express.com/cn/sc/dynamic_function/waybill/#search/bill-number/')

# input_bar = WebDriverWait(browser, 20).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "token-input"))
# )

def get_tracking_num_SF_100(tracking_number, phone_number):
    if phone_number.find('*') != -1:
        return False, 0
    if phone_number.find('.') != -1:
        return False, 0
    if phone_number == '':
        return False, 0
    try:
        input_bar.click()
        input_bar.clear()
        input_bar.send_keys(tracking_number)

        ensure_btn = browser.find_element_by_id('query')
        ensure_btn.click()

        # import time
        # time.sleep(3)

        input = WebDriverWait(browser, 2).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="checkCode"]/div[2]/div/div[2]/input[1]'))
            # EC.visibility_of_element_located
        )

        # input = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="checkCode"]/div[2]/div/div[2]/input[1]'))
        # )
        # input = browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[1]')
        # input = verify_code.find_element_by_xpath('//input[3]')
        ActionChains(browser).send_keys_to_element(input, phone_number[0]).perform()
        input = browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[2]')
        ActionChains(browser).send_keys_to_element(input, phone_number[1]).perform()
        input = browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[3]')
        ActionChains(browser).send_keys_to_element(input, phone_number[2]).perform()
        input = browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[2]/input[4]')
        ActionChains(browser).send_keys_to_element(input, phone_number[3]).perform()

        ensure_btn = browser.find_element_by_xpath('//*[@id="checkCode"]/div[2]/div/div[3]')
        ensure_btn.click()

        # time.sleep(3)

        date = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="queryResult"]/div[3]/div[2]/table/tbody/tr[1]/td[1]'))
        )
        print(date.text)
        return True, date.text
    except (TimeoutException, NoSuchElementException, ElementNotVisibleException, WebDriverException, TypeError):
        print('无法获取')
        # print(browser.page_source)
        return False, 0

    # verify_code.click()
    # verify_code.send_keys('1234')

    # input_bar.clear()


def get_tracking_num_SF(tracking_number):
    input_bar.click()
    input_bar.clear()
    input_bar.send_keys(tracking_number)

    ensure_btn = browser.find_element_by_id('queryBill')
    ensure_btn.click()

    try:
        # import time
        # time.sleep(3)
        iframe = browser.find_element_by_xpath('//frame')  # 找到“嵌套”的iframe
        ts = browser.find_element_by_id('tcaptcha_window')
        # iframe = browser.find_element_by_xpath('//iframe')  # 找到“嵌套”的iframe
        browser.switch_to.frame('tcaptcha_popup')  # 切换到iframe
        ts = browser.find_element_by_class_name('tcaptcha_drag_button')

        verify_code = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tcaptcha_drag_button"))
        )
        # source_element = browser.find_element_by_id('tcaptcha_drag_thumb')

        # 27.5 ~ 228.action = ActionChains(driver)            # 实例化一个action对象
        # action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
        # action.reset_actions()
        # action.move_by_offset(180, 0).perform()  # 移动滑块5
        ActionChains(browser).click_and_hold(verify_code).perform()
        ActionChains(browser).reset_actions().drag_and_drop_by_offset(verify_code, 200, 0).perform()  # 链式用法

        result_info = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result-info2"))
        )
        # table_tr_list = result_info.find_elements_(By.TAG_NAME, "tr")

        table_tr_list = result_info.find_elements_by_class_name('row1')
        # result_info = browser.find_element_by_class_name('result-info')
        last_row = result_info.find_element_by_class_name('last')
        row_1 = last_row.find_element_by_class_name('row1')
        day = row_1.find_element_by_class_name('day')
        time = row_1.find_element_by_class_name('time')
        total_time = day.text + ' T ' + time.text
        print(tracking_number, '时间为{}'.format(total_time))
        return True, total_time
    except (TimeoutException, NoSuchElementException):
        print('无法获取')
        print(browser.page_source)
        return False, 0


def get_tracking_num(tracking_number):
    input_bar.click()
    input_bar.clear()
    input_bar.send_keys(tracking_number)

    ensure_btn = browser.find_element_by_id('query')
    ensure_btn.click()

    try:
        result_info = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result-info"))
        )

        # result_info = browser.find_element_by_class_name('result-info')
        last_row = result_info.find_element_by_class_name('last')
        row_1 = last_row.find_element_by_class_name('row1')
        day = row_1.find_element_by_class_name('day')
        time = row_1.find_element_by_class_name('time')
        total_time = day.text + ' T ' + time.text
        print(tracking_number, '时间为{}'.format(total_time))
        return True, total_time
    except (TimeoutException, NoSuchElementException):
        print('无法获取')
        return False, 0


# DH.20190930.0642-04	顺丰标准快递	"SF1160423969219	"	13522005547	5547

# print(browser.page_source)
if __name__ == '__main__':
    get_tracking_num_SF_100('SF1160423969219', list('5547'))
