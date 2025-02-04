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

from .models import TiktokHashtagsORM
from .models import TiktokSongsORM
from .models import TiktokBreakoutSongsORM
from .models import CookieFile
from tiktokscrapp.settings import BASE_DIR



class TiktokScrapper():

    os.chdir('C:/Users/heppy/Desktop/NEWER-PY-main')

    def __init__(self):
        self.driver = None

    def create_driver(self):
        try:
            with open('ads.tiktok.com.cookies.json', 'r') as f:
                    cookies = json.load(f)
            if not cookies:
                raise FileNotFoundError("Cookie файл не найден")

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
            
            all_windows = self.driver.window_handles
            if all_windows:
                    self.driver.switch_to.window(all_windows[-1])
            else:
                    print("Нет доступных окон!")
        
            try:
                self.driver.get("https://ads.tiktok.com/business/creativecenter/pc/en")
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            except Exception as e:
                print(f"Ошибка при загрузке TikTok: {e}")
                return
            
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Ошибка при добавлении cookie: {e}")

            self.driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en")
            sleep(5)
            self.hashtags_func()

            self.driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
            sleep(5)
            self.songs_func()

            self.driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
            sleep(5)
            self.breakout_func()
        
        except Exception as e:
           print(f"Произошла ошибка: {e}")

        finally:
            if self.driver:  
                try:
                    print("Закрываем браузер...")
                    self.driver.quit()
                except Exception as e:
                    print(f"Ошибка при закрытии браузера: {e}")
                self.driver = None
    

    def smooth_scroll(self,elem: WebElement):
        self.driver.execute_script(
            """arguments[0].scrollIntoView({block: "center", behavior: "smooth"});""", elem
        ) 

    def smooth_click(self,elem: WebElement):
        self.driver.execute_script(
            """arguments[0].click({block: "center", behavior: "smooth"});""", elem
        ) 
        
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
#        for element in hashtags_elements:
#            hashtag_text = element.text
#            hashtags.append(hashtag_text)
#        print(hashtags)
#        hashtags_dict = {i+1: hashtag for i, hashtag in enumerate(hashtags[:100])}
#        json_file_path = 'hashtags.json'
#        with open(json_file_path, 'w') as json_file:
#            json.dump(hashtags_dict, json_file, indent=2)
#        print(f"Хештеги были сохранены в файл: {json_file_path}")
    
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
        #songs_dict = {str(i + 1): {"song_name": song, "author_name": author} for i, (song, author) in enumerate(zip(songs[:100], authors[:100]))}
        #json_file_path = 'songs.json'
        #with open(json_file_path, 'w') as json_file:
        #    json.dump(songs_dict, json_file, indent=2)
        #print(f"Пенси были сохранены в файл: {json_file_path}")

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

        
        
        #breakout_songs_elements = self.driver.find_elements(By.CLASS_NAME,"ItemCard_musicName__2znhM")
        #breakout_songs = []
        #for element in breakout_songs_elements:
        #    breakout_song_text = element.text
        #    breakout_songs.append(breakout_song_text)
        #print(breakout_songs)
        #breakout_author_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")
        #breakout_authors = []
        #for element in breakout_author_elements:
        #    breakout_author_text = element.text
        #    breakout_authors.append(breakout_author_text)
        #print(breakout_authors)
        #if len(breakout_songs) != len(breakout_authors):
        #    raise ValueError("Списки должны быть одинаковой длины")
        #breakout_songs_dict = {str(i + 1): {"song_name": breakout_song, "author_name": breakout_author} for i, (breakout_song, breakout_author) in enumerate(zip(breakout_songs[:100], breakout_authors[:100]))}
        #json_file_path_2 = 'breakout_songs.json'
        #with open(json_file_path_2, 'w') as json_file:
        #    json.dump(breakout_songs_dict, json_file, indent=2)
        #print(f"Второй список песен был сохранен в файл: {json_file_path_2}")
        
        

def main():
    TiktokScrapper().create_driver()

