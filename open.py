from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

from keyboard import wait as keyboard_wait
from datetime import datetime
from sys import exit as sys_exit
from traceback import format_exc


DAY = ['20240803', '20240707'][0]
TIME = 1
TARGET = [
    (2, 4),
    (2, 5)
]
SITE = ['{} 층 {} 구역'.format(_set[0], _set[1]) for _set in TARGET]
CAPTCHA_IMG = 'screenshot.png'
_XPATH = '//*[@id="list_time"]/li[{}]/button/span/span'.format(TIME)
TIME_NAME = '18시 00분'

try:
    # Set Driver #
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    macro_driver = webdriver.Chrome(options=chrome_options)
    _wait = lambda sec: WebDriverWait(macro_driver, sec, poll_frequency=0.1)

    # macro_driver.set_page_load_timeout(0.5)
    # Set Driver #



    print('wait for esc to run')
    keyboard_wait('esc') # For test
    print('running')
    start_time = datetime.now()



    # deal with the first window #
    btn_list = _wait(100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ticketing_process_box > div > div.box_ticketing_process > dl.date_choice > dd.sorting > button.type_list')))
    btn_list.click()
    btn_date = _wait(10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#dateSelect_{} > button > span'.format(DAY))))
    btn_date.click()

    
    # while True:
    #     k = macro_driver.find_element(By.XPATH, _XPATH).get_attribute('class')
    #     print(k)
    #     if DAY in k:
    #         break
    #     else: continue

    btn_time = _wait(10).until(EC.all_of(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="list_time"]/li[{}]/button'.format(TIME)), TIME_NAME)),
        EC.element_to_be_clickable((By.XPATH, '//*[@id="list_time"]/li[{}]/button'.format(TIME))))
    # btn_time.click()
    btn_reservation = _wait(10).until(EC.element_to_be_clickable((By.ID,'ticketReservation_Btn')))
    btn_reservation.click()
    # deal with the first window #



    # deal with the second window #
    _wait(10).until(EC.number_of_windows_to_be(2))
    windows = macro_driver.window_handles
    macro_driver.switch_to.window(windows[1])
    print('new window')

    _wait(10).until(lambda driver: driver.execute_script("return typeof jQuery != 'undefined'"))
    _wait(10).until(lambda driver: driver.execute_script("return jQuery.active == 0"))

    html = macro_driver.page_source
    captcha_pres = False if html.find('id="certification"') == -1 else True


    print('cap', captcha_pres)
    print('waiting')
    keyboard_wait('esc')
    print('second running')


    # Reservation #
    macro_driver.switch_to.frame('oneStopFrame')
    
    area_opens = macro_driver.find_elements(By.CLASS_NAME, 'area_info')
    for _area_open in area_opens: _area_open.click()

    site_names = [_name.text for _name in macro_driver.find_elements(By.CLASS_NAME, 'area_tit')]
    residuals = macro_driver.find_elements(By.CLASS_NAME, 'seat_residual')
    site_len = len(site_names)
    
    for i in range(site_len):
        print(site_names[i], residuals[i].text)

    # Reservation #


except Exception:
    print(format_exc())

finally:
    print('EndTime: {}      RunTime: {}'.format(datetime.now(), datetime.now()-start_time))
    sys_exit(0)
