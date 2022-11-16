import requests
from bs4 import BeautifulSoup as b
from url import URL, dict_
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import json





def get_data_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument('general.useragent.override', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36')

    try:
        driver = webdriver.Chrome(
            executable_path='../ozon/chrome/chromedriver.exe',
            options=options
        )
        driver.get(url)
        time.sleep(10)

        

        # time.sleep(120)
        # delay = 5 # seconds
        # try:
        #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        #     print("Page is ready!")
        # except TimeoutException:
        #     print("Loading took too much time!")

        # try:
        #     time.sleep(10)

        #     element = driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/div')
        #     print('click')
        #     driver.execute_script("arguments[0].click();", element)
        #         #tab-active-index-0 tb-detail w990
        #     name = driver.find_element(By.XPATH, '//*[@id="J_Title"]/h3')
        #     print(name.text)

        #     time.sleep(10)
        # except Exception as ex:
        #     print(ex)

        # with open('index_selenium.html', 'w', encoding='utf-8') as file:
        #     file.write(driver.page_source)
        
        

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()




def main():
    # get_data(URL)
    get_data_with_selenium(URL)



if __name__ == '__main__':
    main()