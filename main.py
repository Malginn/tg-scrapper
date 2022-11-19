import urllib.request
import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.common import NoSuchElementException, TimeoutException

from colorama import Fore


def get_data_with_selenium(link):
    os.chdir('./')
    os.system('start browser.bat')
    time.sleep(3)

    dict_xpath = {'name': '//*[@class="tb-main-title"]',
                  'seller': '//*[@class="tb-shop-name"]',
                  'price': '//*[@class="tb-rmb-num"]',
                  'size': '//*[@data-property="尺码"]/li/a/span',
                  'delivery': '//*[@id="J_WlServiceInfo"]',
                  'color': '//*[@data-property="颜色分类"]/li/a/span',
                  'characteristic': '//*[@class="attributes-list"]/li',
                  'image': '//*[@id="description"]/div/table/tbody/tr/td/img'}

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chrome/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    dict_value = {'name': '',
                  'seller': '',
                  'price': list(),
                  'size': list(),
                  'delivery': '',
                  'color': '',
                  'characteristic': list(),
                  'image': list()
                  }

    try:
        driver.get(link)
        timeout = 40
        WebDriverWait(driver, timeout).until(condition.presence_of_element_located((By.XPATH, dict_xpath['name'])))

    except TimeoutException:
        print(Fore.RED + 'TimeoutException')

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
            prices = driver.find_elements(By.XPATH, dict_xpath['price'])
            for price in prices:
                dict_value['price'].append(price.text)
        except NoSuchElementException:
            print(Fore.RED + 'Price not found')

        try:
            sizes = driver.find_elements(By.XPATH, dict_xpath['size'])
            for size in sizes:
                dict_value['size'].append(size.text)
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
            print(Fore.BLUE + (type(dict_value['color'])))

        try:
            for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
                dict_value['characteristic'].append(characteristic.text)
        except NoSuchElementException:
            print(Fore.RED + 'Characteristics not found')

        try:
            images = driver.find_elements(By.XPATH, dict_xpath['image'])
            for image in images:
                print(type(image))
                ActionChains(driver).move_to_element(image).perform()
                time.sleep(0.5)
                dict_value['image'].append(download(image.get_attribute('src'), images.index(image)))
        except NoSuchElementException:
            print(Fore.RED + 'Images not found')

    finally:

        driver.close()
        driver.quit()
        return dict_value


def download(url, num):
    resource = urllib.request.urlopen(url)
    with open(f"./images/test{num}.jpg", 'wb') as out:
        out.write(resource.read())
    return f'test{num}.jpg'
