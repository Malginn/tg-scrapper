import shutil
import os

def clear_img():
    shutil.rmtree('./images/')
    os.makedirs('./images/')

clear_img()