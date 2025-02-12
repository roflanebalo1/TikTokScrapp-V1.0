from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
import json
import requests
import os
import django
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import urllib3
from contextlib import contextmanager

from SRC.tiktokadmink.DTO import CookieFileORMDTO


from .models import TiktokHashtagsORM
from .models import TiktokSongsORM
from .models import TiktokBreakoutSongsORM
from .models import CookieFileORM
from src.tiktokadmink.core.settings import BASE_DIR



class DriverFactory():
        
    @contextmanager   
    def create_driver(self):

        try:

            chrome_options = Options()
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-webrtc')

            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            prefs = {"webrtc.ip_handling_policy": "disable_non_proxied_udp"}
            chrome_options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            WebDriverWait(self.driver, 10)
            
            #all_windows = self.driver.window_handles
            #if all_windows:
            #        self.driver.switch_to.window(all_windows[-1])
            #else:
            #        print("Нет доступных окон!")
        #
            #try:
            #    self.driver.get("https://ads.tiktok.com/business/creativecenter/pc/en")
            #    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            #except Exception as e:
            #    print(f"Ошибка при загрузке TikTok: {e}")
            #    return
            
            return self.driver
        
        except Exception as e:
            print(f"Произошла ошибка: {e}")

class Repository():

    def load_cookies_from_db(self):

        cookie_file = CookieFileORM.objects.first()

        if cookie_file is None:
            raise Exception("Нет записи CookieFileORM")
        
        cookies_content = cookie_file.content
        cookies = json.loads(cookies_content)
        cookie_dto = CookieFileORMDTO(cookies=cookies)

        return cookie_dto
        




class LoadCookies():

    def load_cookies(self):
            cookies = json.loads(cookies_content)
            for cookie in cookies:
                self.driver.add_cookie(cookie)



class Parser():
    def __init__(self):
        self.browser = DriverFactory()
        self.driver = self.browser.create_driver()
        self.driver = self.browser.load_cookies_from_db() 

    def ScrappInfo(self):
        main_scrapp = MainScrapp(self.driver)
        self.driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en")
        sleep(5)
        main_scrapp.hashtags_func()
        self.driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
        sleep(5)
        main_scrapp.songs_func()
        self.driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
        sleep(5)
        main_scrapp.breakout_func()

    def close_browser(self):
        if self.driver:
            try:
                print("Закрываем браузер...")
                self.driver.quit()
            except Exception as e:
                print(f"Ошибка при закрытии браузера: {e}")
    
class Scrolls_Click():
    def __init__(self, driver):
        self.driver = driver

    def smooth_scroll(self,elem: WebElement):
        self.driver.execute_script(
            """arguments[0].scrollIntoView({block: "center", behavior: "smooth"});""", elem
        ) 

    def smooth_click(self,elem: WebElement):
        self.driver.execute_script(
            """arguments[0].click({block: "center", behavior: "smooth"});""", elem
        ) 

class MainScrapp(Scrolls_Click):
    def __init__(self, driver):
        self.driver = driver

    def hashtags_func(self):
        while True:
            hashtags_elements = self.driver.find_elements(By.CLASS_NAME, "CommonDataList_cardWrapper__kHTJP")
            last_hashtag = hashtags_elements[-1]
            self.smooth_scroll(last_hashtag)
            sleep(3)
            if len(hashtags_elements) == 100:
                break
        hashtags_elements = self.driver.find_elements(By.CLASS_NAME, "CardPc_titleText__RYOWo")
        for element in hashtags_elements:
            hashtag_text = element.text
            TiktokHashtagsORM.objects.get_or_create(name=hashtag_text, value="hashtag")
        print("Хештеги успешно сохранены в базу данных.")
    
    def songs_func(self):
        self.driver.execute_script("window.scrollBy(0,1500)","")
        for i in range(1, 10):
            self.driver.execute_script("window.scrollBy(0,1200)","")
            sleep(4)
        songs_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_musicName__2znhM")
        songs = []
        for element in songs_elements:
            song_text = element.text
            songs.append(song_text)
        print(songs)
        author_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")
        authors = []
        for element in author_elements:
            author_text = element.text
            authors.append(author_text)
        print(authors)
        if len(songs_elements) != len(author_elements):
            raise ValueError("Списки должны быть одинаковой длины")
        for song, author in zip(songs_elements, author_elements):
            song_text = song.text
            author_text = author.text
            TiktokSongsORM.objects.get_or_create(name=song_text, author=author_text)
        print("Песни успешно сохранены в базу данных.")

    def __song_links(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "index-mobile_goToDetailBtnWrapper__puubr")))

        song_elements = self.driver.find_elements(By.CLASS_NAME, "index-mobile_goToDetailBtnWrapper__puubr")

        song_links = [song.get_attribute("href") for song in song_elements if song.get_attribute("href")]

        print("Найденные ссылки на песни:")
        for link in song_links:
            print(link)

    def __update_url_period(url, new_period=120):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['period'] = [str(new_period)]
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed_url._replace(query=new_query))
    
    def __update_links(update_url_period, song_links):
        updated_song_links = [update_url_period(link) for link in song_links]
        for link in updated_song_links:
            print(link)


    def breakout_func(self):
        self.driver.execute_script("window.scrollBy(13500,0)","")
        breakout_button = self.driver.find_elements(By.CLASS_NAME, "ContentTab_itemLabelText__hiCCd")
        breakout_click = breakout_button[1]
        self.smooth_click(breakout_click)
        sleep(5)
        for i in range(1, 10):
            self.driver.execute_script("window.scrollBy(0,1200)","")
            sleep(4)

        breakout_songs_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_musicName__2znhM")
        breakout_author_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")

        if len(breakout_songs_elements) != len(breakout_author_elements):
            raise ValueError("Списки должны быть одинаковой длины")

        for breakout_song, breakout_author in zip(breakout_songs_elements, breakout_author_elements):
            breakout_song_text = breakout_song.text
            breakout_author_text = breakout_author.text
            TiktokBreakoutSongsORM.objects.get_or_create(name=breakout_song_text, author=breakout_author_text)
        print("Второй список песен успешно сохранен в базу данных.")


def main(): 
    Parser()

