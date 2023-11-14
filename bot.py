# Import required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from config import *
import os
import time

# Setting the path to the directory with images
path = os.path.abspath("image")

# Configuring browser settings and instantiating the Chrome driver
options = Options()
options.add_argument("log-level=3")

options.add_argument("--disable-blink-features=AutomationControlled")
service = Service()
browser = webdriver.Chrome(service=service, options=options)


def find_element_page(xpath, send=None, click_1=False, click_2=False, error='Error', timer=10):
    try:
        el = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(browser, timer).until(el)
        element = browser.find_element(By.XPATH, xpath)
        if send:
            element.send_keys(send)
        if click_1:
            browser.execute_script("arguments[0].click();", element)
        if click_2:
            element.click()
        return True
    except TimeoutException:
        if error == "Error":
            print(xpath, error)
        else:
            print(error)

        return False
    except Exception as ex:
        print(ex, xpath)
# The find_element_page function is used to find elements on a page using XPath, with the ability to send text, perform a click, and handle errors using a try-except block
# If the search for an element is successful, the function returns True, otherwise - False


# Opening the DeviantArt site login page and entering user credentials
browser.get("https://www.deviantart.com/users/login")
find_element_page("//input[@name='username']", send=login)
find_element_page("//input[@id='password']", send=password)

find_element_page("//button[.='Log In']", click_1=True)

time.sleep(2)

# Start uploading images from the specified directory to the DeviantArt website
for image in os.listdir("image"):

    browser.get("https://www.deviantart.com/submit/")

    if find_element_page("//span[@class='submit-tab-close']", click_1=True, error="", timer=2):
        time.sleep(2)

    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "(//iframe)[2]")))
# Selecting an image to upload
    print(image)
    browser.find_elements(By.XPATH, "//input[@name='file']")[1].send_keys(path + "\\" + image)

    time.sleep(2)

    find_element_page(f"//span[.='{size}']", click_1=True, error="Нет данного размера", timer=4)
# Adding a description and tags to an image
    if watermark:
        find_element_page("//input[@class='ile-watermark']", click_1=True)

    find_element_page("//div[@class='ccwriter-content']", click_2=True)

    find_element_page("//div[@class='writer selectable no-lub put-art-here ui-droppable']", send=description)
    find_element_page("//div[@data-input-type='tag']", send=tags)

    find_element_page(f"(//input[@value='{tools}'])[1]", click_1=True)
    find_element_page(f"(//input[@value='{datasets}'])[2]", click_1=True)

    if mature_content:
        find_element_page("//input[@id='ile-mature-input-yes']", click_1=True)
        for click__1 in mature_content:
            find_element_page(f"//label[.='{click__1}']", click_1=True)

    time.sleep(2)

    if scraps:
        find_element_page("//input[@id='ile-scraps-input-yes']", click_1=True)
# Selecting options and tools
    if gallery:
        find_element_page("//span[.='Gallery and Group options']", click_1=True)
        time.sleep(1)
        for click__2 in gallery:
            find_element_page(f"//label[.='{click__2}']", click_1=True)

    if not find_element_page("//div[@class='ile-feature ile-feature-premium-content disabled']", click_1=True):
        find_element_page("//div[@class='ile-feature ile-feature-premium-content has-default']", click_1=True)
        time.sleep(1)
        find_element_page("//div[@class='ile-feature ile-feature-premium-content disabled']", click_1=True)

    find_element_page("//button[@class='ile-button ile-continue-button smbutton smbutton-green']", click_1=True)
# Setting prices for paid downloads
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='paid-downloads-price']")))

    find_element_page("//input[@id='paid-downloads-price']", send=Keys.CONTROL + "a" + Keys.BACKSPACE)
    find_element_page("//input[@id='paid-downloads-price']", send=points)

    find_element_page("//span[.='Submit Now']", click_1=True)
    time.sleep(2)


browser.quit()
