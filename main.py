import os
import shutil
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

dict_xpath = {'name': '',
              'seller': '',
              'price': '',
              'size': '',
              'delivery': '',
              'color': '',
              'characteristic': '',
              'image': ''}

dict_value = dict()


def get_data_with_selenium(link):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chrome/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    try:
        driver.get(link)
        time.sleep(10)
        dict_value['name'] = driver.find_element(By.XPATH, dict_xpath['name']).text
        dict_value['seller'] = driver.find_element(By.XPATH, dict_xpath['seller']).text
        dict_value['price'] = driver.find_element(By.XPATH, dict_xpath['price']).text
        dict_value['size'] = driver.find_element(By.XPATH, dict_xpath['size']).text
        dict_value['delivery'] = driver.find_element(By.XPATH, dict_xpath['delivery']).text
        dict_value['color'] = driver.find_element(By.XPATH, dict_xpath['color']).text

        characteristics = list()
        for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
            characteristics.append(characteristic.text)
        print(dict_value)

        clear_img()
        images = driver.find_elements(By.XPATH, dict_xpath['image'])
        for image in images:
            download(image.get_attribute('src'), images.index(image))

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


def download(url, i):
    resource = urllib.request.urlopen(url)
    out = open(f"./images/image_{i}.jpg", 'wb')
    out.write(resource.read())
    out.close()


def clear_img():
    shutil.rmtree('./images')
    os.makedirs('./images')


def main():
    link = ''
    get_data_with_selenium(link)


if __name__ == '__main__':
    main()
