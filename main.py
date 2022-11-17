import urllib.request
import base64
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from colorama import Fore

import time

dict_xpath = {'name': '',
              'seller': '',
              'price': '',
              'size': '',
              'delivery': '',
              'color': '',
              'characteristic': '',
              'image': ''}


def get_data_with_selenium(link):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chrome/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    dict_value = {'name': '',
                  'seller': '',
                  'price': '',
                  'size': '',
                  'delivery': '',
                  'color': '',
                  'characteristic': list(),
                  'image': list()
                  }
    try:
        driver.get(link)
        time.sleep(10)

    except Exception as ex:
        print(ex)

    else:
        try:
            dict_value['name'] = driver.find_element(By.XPATH, dict_xpath['name']).text
        except NoSuchElementException:
            print(Fore.RED + 'Name not found')

        try:
            dict_value['seller'] = driver.find_element(By.XPATH, dict_xpath['seller']).text
        except NoSuchElementException:
            print(Fore.RED + 'Seller not found')

        try:
            dict_value['price'] = driver.find_element(By.XPATH, dict_xpath['price']).text
        except NoSuchElementException:
            print(Fore.RED + 'Price not found')

        try:
            dict_value['size'] = driver.find_element(By.XPATH, dict_xpath['size']).text
        except NoSuchElementException:
            print(Fore.RED + 'Size not found')

        try:
            dict_value['delivery'] = driver.find_element(By.XPATH, dict_xpath['delivery']).text
        except NoSuchElementException:
            print(Fore.RED + 'Delivery not found')

        try:
            dict_value['color'] = driver.find_element(By.XPATH, dict_xpath['color']).text
        except NoSuchElementException:
            print(Fore.RED + 'Color not found')

        try:
            for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
                dict_value['characteristic'].append(characteristic.text)
        except NoSuchElementException:
            print(Fore.RED + 'Characteristics not found')

        try:
            images = driver.find_elements(By.XPATH, dict_xpath['image'])
            for image in images:
                dict_value['image'].append(download(image.get_attribute('src')))
        except NoSuchElementException:
            print(Fore.RED + 'Images not found')

    finally:
        driver.close()
        driver.quit()
        dump = json.dumps(dict_value)
        return dump


def download(url):
    resource = urllib.request.urlopen(url)
    image = base64.b64encode(resource.read())
    # for decode use:
    # base64.b64decode(image)
    return image


def main():
    link = ''
    dump = get_data_with_selenium(link)
    print(Fore.YELLOW + 'dump finally ready')
    print(Fore.GREEN + f'Result: {dump}')


if __name__ == '__main__':
    main()
