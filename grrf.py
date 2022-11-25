# import shutil
# import os

# def clear_img():
#     shutil.rmtree('./images/')
#     os.makedirs('./images/')

# clear_img()

import requests
import json
import numpy as np
url = 'http://tds.alicdn.com/json/item_imgs.htm?t=desc/icoss1533006878543ae5df89790cfc&sid=23633267&id=677687193050&s=7c8024a7689bdc312f9e53630f7cadd1&v=2&m=1'
# image_json = driver.execute_script("return Hub.config.get('desc').apiImgInfo")
r = requests.get(url)
image_fucking_dict = json.loads(r.text[14:-1])
# print(image_fucking_dict.keys())
image_name_list = []
for k in image_fucking_dict.keys():
    image_name_list.append(k)
print(image_name_list[4:])
