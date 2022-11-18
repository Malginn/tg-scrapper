import urllib.request
import base64
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.common import NoSuchElementException, TimeoutException

from colorama import Fore

import time

from selenium.webdriver.support.wait import WebDriverWait


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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6*2);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6*3);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6*4);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6*5);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
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

        try:
            for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
                dict_value['characteristic'].append(characteristic.text)
        except NoSuchElementException:
            print(Fore.RED + 'Characteristics not found')

        try:
            images = driver.find_elements(By.XPATH, dict_xpath['image'])
            for num, image in enumerate(images):
                dict_value['image'].append(download(image.get_attribute('src'), num))
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
    

    # image = base64.b64encode(resource.read())
    # for decode use:
    # base64.b64decode(image)


def main(text='https://item.taobao.com/item.htm?id=687815414870&price=194.99&sourceType=item&sourceType=item&suid=f4ab6dfd-3c89-4606-81a7-b9b74ad5adb9&ut_sk=1.YgbGi%2FkQyU0DAD3WQG9i%2BcAZ_21646297_1668264784118.Copy.ShareGlobalNavigation_1&un=75b8c07d63d793d3b869032d15dddb3f&share_crt_v=1&un_site=0&spm=a2159r.13376460.0.0&sp_abtk=gray_ShareGlobalNavigation_1_code_simpleAndroid&tbSocialPopKey=shareItem&sp_tk=dDZDYmQxck1TdW4%3D&cpp=1&shareurl=true&short_name=h.UgFnSN4&bxsign=scd7fVjWiuAdaVF9IWPRnH-aVCofWKHVNbA9YOC3YWLrrDMwNZgLit2jZUBIBDj6aNhOlcPfcXr_odogmSCQeRh6J4dKjZVoBf6uA-NLYQRYgB-5yC2nYyX5N4fDyv9RViOgmgYDKfBaP4phh2IL6qczQ&tk=t6Cbd1rMSun&app=chrome&price=194.99&sourceType=item&sourceType=item&suid=f4ab6dfd-3c89-4606-81a7-b9b74ad5adb9&ut_sk=1.YgbGi%2FkQyU0DAD3WQG9i%2BcAZ_21646297_1668264784118.Copy.ShareGlobalNavigation_1&un=75b8c07d63d793d3b869032d15dddb3f&share_crt_v=1&un_site=0&spm=a2159r.13376460.0.0&sp_abtk=gray_ShareGlobalNavigation_1_code_simpleAndroid&tbSocialPopKey=shareItem&sp_tk=dDZDYmQxck1TdW4%3D&cpp=1&shareurl=true&short_name=h.UgFnSN4&bxsign=scd7fVjWiuAdaVF9IWPRnH-aVCofWKHVNbA9YOC3YWLrrDMwNZgLit2jZUBIBDj6aNhOlcPfcXr_odogmSCQeRh6J4dKjZVoBf6uA-NLYQRYgB-5yC2nYyX5N4fDyv9RViOgmgYDKfBaP4phh2IL6qczQ&tk=t6Cbd1rMSun&app=chrome'):
    link = text
    dict_ = get_data_with_selenium(link)
    # images = dict_['image']
    # for img in images:
    #     await message.answer_photo(base64.b64decode(img))
    print(Fore.GREEN + 'dump finally ready')

    return dict_


if __name__ == '__main__':
    main()
