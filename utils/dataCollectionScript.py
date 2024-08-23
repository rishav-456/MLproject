import pyautogui as gui
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utitlity import shapeIdentifiyer
import pandas as pd
from constants import URL

# This python script automates the process of interacting with a web
# application located at the URL "https://me.meshcapade.com/editor" for the purpose of data collection.

def enterValue(element:WebElement, value:int):
    """
    The function `enterValue` is used to enter an integer value into a web element and perform a series
    of actions.
    
    :param element: The `element` parameter in the `enterValue` function is of type `WebElement`, which
    represents an element on a web page. This element can be interacted with using various methods such
    as clicking, sending keys, etc
    :type element: WebElement
    :param value: The `value` parameter in the `enterValue` function is an integer that represents the
    value you want to enter into a web element on a webpage
    :type value: int
    """
    element.click()
    gui.hotkey("ctrl","a")
    element.send_keys(f"{value}")
    driver.find_element(by=By.CSS_SELECTOR, value='button[class="editorMotion_subTab__5irbg ui-label-regular editorMotion_active__S8SMV"]').click()

driver = Chrome()
driver.get(URL)
driver.maximize_window()

gui.alert("Starting...")

height = driver.find_element(By.CSS_SELECTOR, value='''input[name="Height"]''')
chest = driver.find_element(By.CSS_SELECTOR, value='''input[name="Bust_girth"]''')
waist = driver.find_element(By.CSS_SELECTOR, value='''input[name="Waist_girth"]''')
hips = driver.find_element(By.CSS_SELECTOR, value='''input[name="Top_hip_girth"]''')
myData = []
i = 1
try:
    # This block of code is a nested loop structure that iterates through different ranges of values
    # for height, chest, waist, and hips measurements.
    for h in range(65,71):
        enterValue(height,h)
        for c in range(32,46):
            enterValue(chest,c)
            for w in range(30,41,2):
                enterValue(waist,w)
                for hi in range(32,46):
                    enterValue(hips, hi)
                    shape = shapeIdentifiyer(c,w,hi,"inches")
                    print(shape)
                    driver.find_element(by=By.CSS_SELECTOR, value='button[class="editorMotion_subTab__5irbg ui-label-regular editorMotion_active__S8SMV"]').click()
                    weight = float(driver.find_element(By.CSS_SELECTOR, value='''input[name="Weight"]''').get_attribute("value"))
                    x1,y1 = (780,232)
                    x2,y2 = (1208,960)
                    path =f"utils/data/{shape.lower()}/{i}.png"
                    gui.screenshot(path,[x1,y1,x2-x1,y2-y1])
                    myData.append([h,weight,c,w,hi,shape.lower(),path])
                    i+=1

except Exception as e:
    print(e)
finally:
    df = pd.DataFrame(myData, columns="height weight bust waist hip shape img".split())
    df.to_csv("utils\data\data.csv",index=False)

gui.alert("Closing...")