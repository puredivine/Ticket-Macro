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


day = ['20240623', '20240523', '20240629'][2]
captcha_img = 'screenshot.png'

try:
    read_capt = Buildment().captcha_cracker

    print('wait for esc to run')
    keyboard.wait('esc') # For test
    print('running')

    # main driver set up #
    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # Add later : ignore alerts
    macro_driver = webdriver.Chrome(options=option)
    _wait = lambda sec: WebDriverWait(macro_driver, sec, poll_frequency=0.5)


    # deal with the first window #
    date = _wait(100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#dateSelect_{} > button > span'.format(day))))
    date.click()
    _wait(10).until(EC.invisibility_of_element((By.CSS_SELECTOR, '#section_time > div > p')))
    macro_driver.find_element(By.CSS_SELECTOR, '#ticketReservation_Btn').click()


    # deal with the second window #
    _wait(10).until(EC.number_of_windows_to_be(2))
    macro_driver.switch_to.window(macro_driver.window_handles[1])
    
    ##################################################################
    _wait(10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')
    print('Loaded')


    Captcha = macro_driver.execute_script('''return document.querySelector("#certification > div.la_header > div > h3")''')
    print(Captcha)
    print('Captcha', Captcha != None)

    if Captcha != None:
        # Captcha Cracking
        for i in range(1, 100):
            macro_driver.find_element(By.ID, 'captchaImg').screenshot(captcha_img)
            x = read_capt(captcha_img)
            macro_driver.find_element(By.CSS_SELECTOR, '#label-for-captcha').send_keys(x, Keys.ENTER)
            print('captcha try :', i)

            print(macro_driver.execute_script('return document.readyState;'))
            if macro_driver.find_element(By.CSS_SELECTOR, '#errorMessage').is_displayed():
                macro_driver.find_element(By.CSS_SELECTOR, '#btnReload').send_keys(Keys.ENTER)
                macro_driver.find_element(By.CSS_SELECTOR, '#label-for-captcha').clear()
            else:
                break
        print("Captcha cracked")



    _exit('Successfully End At {}'.format(datetime.now()))

# print('captcha broke')
except KeyboardInterrupt:
    raise Exception('==========================KeyboardInterrupt=========================')
    _exit('End At {}'.format(datetime.now()))
