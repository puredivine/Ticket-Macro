from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import keyboard
from datetime import datetime
from sys import exit as _exit
from buildment import Buildment
from time import sleep


DAY = ['20240623', '20240523', '20240629'][1]
MAX_RSV = 1
FLOOR = [1]
SPOT = [12]
SITE = ['{} 층 {} 구역'.format(FLOOR[k], SPOT[k]) for k in range(len(FLOOR))]

CAPTCHA_IMG = 'screenshot.png'
BD = Buildment()
SCIRPT = """
var rects = document.getElementsByTagName('rect');
var result = [];
for (var i = 0; i < rects.length; i++) {
    var rect = rects[i];
    var color = rect.getAttribute("fill");
    var width = rect.getAttribute("width");
    var height = rect.getAttribute("height");
    if (width == 11 && height == 11 && color !== '#DDDDDD') {
        result.push(rect);
    }
}
return result;
"""




try:

    print('wait for esc to run')
    keyboard.wait('esc') # For test
    print('running')



    # main driver set up #
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    macro_driver = webdriver.Chrome(options=chrome_options)
    _wait = lambda sec: WebDriverWait(macro_driver, sec, poll_frequency=0.4)



    # deal with the first window #
    date = _wait(100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#dateSelect_{} > button > span'.format(DAY))))
    date.click()
    _wait(10).until(EC.invisibility_of_element((By.CSS_SELECTOR, '#section_time > div > p')))
    macro_driver.find_element(By.CSS_SELECTOR, '#ticketReservation_Btn').click()



    # deal with the second window #
    _wait(10).until(EC.number_of_windows_to_be(2))
    macro_driver.switch_to.window(macro_driver.window_handles[1])
    
    _wait(10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')
    print('Pop-up Loaded', '\n')
    


    # search remain seats #
    #keyboard.wait('esc')
    print('After Captcha')
    sleep(1) #################################### error 
    macro_driver.switch_to.frame('oneStopFrame')
    
    area_opens = macro_driver.find_elements(By.CLASS_NAME, 'area_info')
    for _area_open in area_opens: _area_open.click()

    site_names = [_name.text for _name in macro_driver.find_elements(By.CLASS_NAME, 'area_tit')]
    residuals = macro_driver.find_elements(By.CLASS_NAME, 'seat_residual')
    site_len = len(site_names)
    


    # Prior
    seat_rsv_cnt = 0
    for _target in SITE:
        idx = site_names.index(_target)
        if seat_rsv_cnt >= MAX_RSV: break
        elif residuals[idx].text != '0석':
            residuals[idx].click()

            seats = macro_driver.execute_script(SCIRPT)
            seats[0].click()
            seat_rsv_cnt += 1
    
    # Not Prior
    if seat_rsv_cnt < MAX_RSV: 
        for i in range(site_len):
            if seat_rsv_cnt >= MAX_RSV: break
            elif residuals[i].text != '0석':
                residuals[i].click()

                seats = macro_driver.execute_script(SCIRPT)
                seats[0].click()
                seat_rsv_cnt += 1
                

    
    # Final Reservation #
    reservation_btn = _wait(10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#nextTicketSelection')))
    reservation_btn.click()

    _wait(10).until(EC.alert_is_present())
    macro_driver.switch_to.alert.accept()

    # EXIT PROGRAM #
    _exit('Successfully End At {}'.format(datetime.now()))

# print('captcha broke')
except Exception as EXC:
    if EXC is KeyboardInterrupt:
        raise Exception('==========================KeyboardInterrupt=========================')
    else:
        raise Exception(EXC)
    _exit('End At {}'.format(datetime.now()))
    
