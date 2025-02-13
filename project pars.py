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
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import urllib3
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class BaseScrapper():
    def __init__(self) -> None:
        pass

    http = urllib3.PoolManager()

    
    @staticmethod
    def create_driver():
        try:
            with open('ads.tiktok.com.cookies.json', 'r') as f:
                cookies = json.load(f)
                sleep(5)

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
            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()

            driver.get("https://ads.tiktok.com/business/creativecenter/pc/en")
            for cookie in cookies:
                driver.add_cookie(cookie)

            #driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en")
            #sleep(10)

            hashtags_scrapper = HashtagsScrapper(driver)
            #hashtags_scrapper.hashtags_func()

            driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
            sleep(10)

            hashtags_scrapper.songs_func()
            #hashtags_scrapper.breakout_func()
            



            while True:
                sleep(10)
        except KeyboardInterrupt:
            driver.quit()


class HashtagsScrapper(BaseScrapper):
    def __init__(self, driver) -> None:
        super().__init__()
        self.driver = driver
    

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
        hashtags = []
        for element in hashtags_elements:
            hashtag_text = element.text
            hashtags.append(hashtag_text)
        print(hashtags)
        hashtags_dict = {i+1: hashtag for i, hashtag in enumerate(hashtags[:100])}
        json_file_path = 'hashtags.json'
        with open(json_file_path, 'w') as json_file:
            json.dump(hashtags_dict, json_file, indent=2)
        print(f"Хештеги были сохранены в файл: {json_file_path}")
    
    def songs_func(self):
        #self.driver.execute_script("window.scrollBy(0,1500)","")
        #for i in range(1, 10):
        #    self.driver.execute_script("window.scrollBy(0,1200)","")
        #    sleep(4)
        #songs_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_musicName__2znhM")
        #first_song = songs_elements[-100]
        #songs = []
        #for element in songs_elements:
        #    song_text = element.text
        #    songs.append(song_text)
        #print(songs)
        #author_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")
        #authors = []
        #for element in author_elements:
        #    author_text = element.text
        #    authors.append(author_text)
        #print(authors)
        #if len(songs_elements) != len(author_elements):
        #    raise ValueError("Списки должны быть одинаковой длины")
        #songs_dict = {str(i + 1): {"song_name": song, "author_name": author} for i, (song, author) in enumerate(zip(songs[:100], authors[:100]))}
        #json_file_path = 'songs.json'
        #with open(json_file_path, 'w') as json_file:
        #    json.dump(songs_dict, json_file, indent=2)
        #print(f"Пенси были сохранены в файл: {json_file_path}")
        #self.driver.execute_script("window.scrollBy(13500,0)","")
        print("Пенси были сохранены в файл:")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "index-mobile_goToDetailBtnWrapper__puubr")))

        song_elements = self.driver.find_elements(By.CLASS_NAME, "index-mobile_goToDetailBtnWrapper__puubr")

        song_links = [song.get_attribute("href") for song in song_elements if song.get_attribute("href")]


        # Выводим результат
        print("Найденные ссылки на песни:")
        for link in song_links:
            print(link)

        def update_url_period(url, new_period=120):
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            query_params['period'] = [str(new_period)]
            new_query = urlencode(query_params, doseq=True)
            return urlunparse(parsed_url._replace(query=new_query))

        updated_song_links = [update_url_period(link) for link in song_links]

        for link in updated_song_links:
            print(link)




        #songs_buttons = self.driver.find_elements(By.CLASS_NAME, "GoDetailBtn_text__UNL0i")
        #songs_click = songs_buttons[0]
        #self.smooth_click(songs_click)
        #sleep(5)
        #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "byted-input-inner__wrapper")))
        #day_button = self.driver.find_elements(By.CLASS_NAME, "byted-input-inner__wrapper")
        #day_click = day_button[0]
        #self.smooth_click(day_click)
        #sleep(5)
        #various_days_buttons = self.driver.find_elements(By.CLASS_NAME, "creative-component-single-line")
        #for i, button in enumerate(various_days_buttons):
        #    text = self.driver.execute_script("return arguments[0].innerText;", button)
        #    print(f"Индекс {i}: '{text}'")
        #print(various_days_buttons)
        #days_click = various_days_buttons[2]
        #self.smooth_click(days_click)

        

    def breakout_func(self):
        self.driver.execute_script("window.scrollBy(13500,0)","")
        breakout_button = self.driver.find_elements(By.CLASS_NAME, "ContentTab_itemLabelText__hiCCd")
        breakout_click = breakout_button[1]
        self.smooth_click(breakout_click)
        sleep(5)
        for i in range(1, 10):
            self.driver.execute_script("window.scrollBy(0,1200)","")
            sleep(4)
        breakout_songs_elements = self.driver.find_elements(By.CLASS_NAME,"ItemCard_musicName__2znhM")
        breakout_songs = []
        for element in breakout_songs_elements:
            breakout_song_text = element.text
            breakout_songs.append(breakout_song_text)
        print(breakout_songs)
        breakout_author_elements = self.driver.find_elements(By.CLASS_NAME, "ItemCard_autherName__gdrue")
        breakout_authors = []
        for element in breakout_author_elements:
            breakout_author_text = element.text
            breakout_authors.append(breakout_author_text)
        print(breakout_authors)
        if len(breakout_songs) != len(breakout_authors):
            raise ValueError("Списки должны быть одинаковой длины")
        breakout_songs_dict = {str(i + 1): {"song_name": breakout_song, "author_name": breakout_author} for i, (breakout_song, breakout_author) in enumerate(zip(breakout_songs[:100], breakout_authors[:100]))}
        json_file_path_2 = 'breakout_songs.json'
        with open(json_file_path_2, 'w') as json_file:
            json.dump(breakout_songs_dict, json_file, indent=2)
        print(f"Второй список песен был сохранен в файл: {json_file_path_2}")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #while True:
        #    find_more_element = self.driver.find_element(By.CLASS_NAME, "CommonDataList_cardWrapper__kHTJP")
        #    print(find_more_element)
#
        #    if self.driver.find_element(By.CLASS_NAME, "CardPc_detail__Y92if"):
        #        with open("hashtags-list.html", "w", encoding="utf-8") as file: 
        #            file.write(self.driver.page_source)
        #        
        #        break
        #    else:
        #        actions = ActionChains(self.driver)
        #        actions.move_to_element(find_more_element).perform()
        #        sleep(3)




BaseScrapper().create_driver()


