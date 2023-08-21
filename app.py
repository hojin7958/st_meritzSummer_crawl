import streamlit as st

from PIL import Image
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument("windows-size=1920x1080")
chrome_options.add_argument("disable-gpu")
import time
import os
from webdriver_manager.chrome import ChromeDriverManager

@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)




st.header("이미지파일로 다운로드")

clicked = st.button("전체받기")

if clicked:

    current_folder = os.getcwd()
    image_folder = 'imgs'

    save_folder = os.path.join(current_folder,image_folder)


    # chrome_path = r'C:\Chrome\chromedriver.exe'
    # service = Service(executable_path=chrome_path)

    driver = get_driver()

    url = 'https://meritzsummer.streamlit.app'
    driver.get(url)

    time.sleep(15)


    driver.switch_to.frame(0)


    def listup_managername(jijum):
        p = '//*[@id="root"]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[2]/div/div[1]/div/div[3]/div/div/div/div[1]/div[2]/input'
        driver.find_element(By.XPATH,p).send_keys(jijum, Keys.ENTER)
        time.sleep(0.5)
        p = '//*[@id="root"]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[2]/div/div[1]/div/div[4]/div/div/div/div[1]'
        driver.find_element(By.XPATH,p).click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        targets = soup.find_all("div","css-8ojfln e1gc5fo21")
        targets2 = []
        for i in targets:
            targets2.append(i.text)

        return targets2


    manager_names = listup_managername('GA2-3지점')
    for name in manager_names:
        save_name = str(name) +".png"    
        p = '//*[@id="root"]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[2]/div/div[1]/div/div[4]/div/div/div/div[1]/div[2]/input'
        driver.find_element(By.XPATH,p).send_keys(name, Keys.ENTER)
        action = ActionChains(driver)
    #     p = '//*[@id="meritz-summer-event-20230820"]/div/span'
        p = '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div[1]/div[1]/div/div[11]/div'
        move_to = driver.find_element(By.XPATH,p)
        action.move_to_element(move_to).perform()
        driver.set_window_size(1200,1024)
        driver.save_screenshot(save_name)
        img = Image.open(save_name) 
        left = 400
        top = 130
        right = 1100
        bottom = 650
        img_res = img.crop((left, top, right, bottom)) 
        img_res.save(save_name)
        st.image(save_name)