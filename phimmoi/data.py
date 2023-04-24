# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib
import uuid
import datetime
from urllib.parse import quote
url = 'https://phimmoiy.net/phim-le'
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import random
from datetime import date
import datetime
import pandas as pd
import time

# Tải nội dung trang web
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
driver = webdriver.Chrome()

movie = []
episodie = []

detail_actor =[]
actossssr =[]
genre = []
genredetail = []
languages=[ "Tiếng Việt","Tiếng Anh",  "Tiếng Trung" , "Tiếng Hàn"
   
 
    

]
count = 0
countrys = []
# Tìm tất cả các thẻ div có class là "owl-item" bên trong thẻ div có class là "owl-wrapper"
items = soup.select('.movies')
idfilm = 1
idgenre = 1
idactor = 1
idepisodie  = 1
# Lặp qua từng item và lấy thông tin
for item in items:
    
# Phân tích các giá trị ngày tháng từ chuỗi đã cho
 
    avatar  = item.select_one('img')['src']
    namefilm = item.select_one('.data').text
    language = random.randint(1,4)
    href  = item.select_one('a')['href']
    status  = "Đã hoàn thành"
    

# Đường dẫn đến thư mục lưu hình ảnh
  

    # Đường dẫn đến thư mục lưu hình ảnh
  

  
    if(avatar!=None):
        print(avatar)
        print(namefilm)
        print(href)
    #lấy name avatar và href
    # save_directory = 'phimmoiy_posters'
    # image_filename = os.path.basename(poster)
    # image_path = os.path.join(save_directory, image_filename)
    # response = requests.get(poster)
    # with open(image_path, 'wb') as f:
    #     f.write(response.content)
         
        responses = requests.get(href)
        if response.ok:
            s = BeautifulSoup(response.text, 'html.parser') 
            # date = extra.select_one('.date').text
            # runtime = extra.select_one('.runtime').text
            # country = extra.select_one('.country').text
            # print(date)
            # print(runtime)
            # print(country)
            #lấy link video url

        
            try:
                driver.get(href)
                driver.implicitly_wait(10)
                video_element = driver.find_element(By.CLASS_NAME, 'metaframe')
                video_url = video_element.get_attribute('src')
                print(video_url)
            except:
                print("Không tìm thấy đường dẫn, tiếp tục với video tiếp theo")
                continue
              
            extra = driver.find_elements(By.CLASS_NAME, 'extra')[1]
            extra_html = extra.get_attribute('innerHTML')
            extra_html = BeautifulSoup(extra_html, 'html.parser')   
            date_str = extra_html.select_one('.date').text
            runtime = extra_html.select_one('.runtime').text
            country = extra_html.select_one('.country').text
            date = datetime.datetime.strptime(date_str, "%b. %d, %Y")
            if country in countrys:
                countryid = countrys.index(country)
            else:
                countrys.append(country)
                countryid = countrys.index(country)
        # Chuyển đổi định dạng ngày tháng
            formatted_date = date.strftime("%Y-%m-%d")
                #lấy description
            wp_content = driver.find_element(By.CLASS_NAME, 'wp-content').get_attribute('innerHTML')
            episodie.append({
                    "description":wp_content,
                    "name": namefilm,
                    "number": 1,
                    "url": video_url,
                    "movie_id": idfilm
                })
            
                #lấy trailer
            cast_div = driver.find_element(By.ID, 'cast')
            sgeneros = driver.find_element(By.CLASS_NAME, 'sgeneros')
            sgeneros_html = sgeneros.get_attribute('innerHTML')
            sgenero = BeautifulSoup(sgeneros_html, 'html.parser')
            gen = sgenero.select('a')
            for s in gen:
                if s in genre:
                    genredetail.append({"movieid" :idfilm , "genre" :genre.index(s)})
                else:
                    genre.append(s)
                    genredetail.append({"movieid" :idfilm , "genre" :genre.index(s)})

                print(s.text)
            cast_html = cast_div.get_attribute('innerHTML')

            soup = BeautifulSoup(cast_html, 'html.parser')

            actors = soup.select('div.person')
            count = 0
            for actor in actors:
                if count == 0:
                    daodien =  actor.select_one('div.name a').text
                    count += 1
                else:
                    name = actor.select_one('div.name a').text
                    print(name)            
                    if actor in actossssr:
                        detail_actor.append({"movieid" :idfilm , "actor" :actossssr.index(name)})
                    else:
                        actossssr.append(name)
                        detail_actor.append({"movieid" :idfilm , "actor" :actossssr.index(name)})            

                # Tìm kiếm trailer trên YouTube
            query = f"{namefilm} trailer"
            query_encoded = quote(query)
            url = f"https://www.youtube.com/results?search_query={query_encoded}"
            driver.get(url)

            trailler = driver.find_element(By.CSS_SELECTOR, 'a#video-title')
            trailer_url =  trailler.get_attribute('href')
                #lấy ảnh
            response = requests.get(trailer_url)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            img_tag = soup.find('meta', property='og:image')
            if img_tag:
                img_url = img_tag['content']
                save_directory = 'posters/'
                  
                    
                if not os.path.exists(save_directory):
                    os.makedirs(save_directory)

                image_filename ="posters" +str(random.randint(1,10000000)) +os.path.basename(avatar)

                image_pathposter = os.path.join(save_directory, image_filename)
                print(image_pathposter)
                response = requests.get(img_url)

                    # Lưu ảnh vào thư mục
                with open(image_pathposter, 'wb') as f:
                    f.write(response.content)    
                print(img_url)
            else:
                print('Không tìm thấy ảnh chính của video')   
            save_directory = 'posters/'
        # Lấy tên file hình ảnh từ URL
            image_filename = os.path.basename(avatar)
                # Tạo đường dẫn đến file hình ảnh trong thư mục lưu trữ
            image_path = os.path.join(save_directory, image_filename)
                # Tải hình ảnh từ URL và lưu vào file trong thư mục lưu trữ
            response = requests.get(avatar)
            try:
                response.raise_for_status()
                with open(image_path, 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.HTTPError as e:
                    print(f"Error downloading image: {e}")
            except Exception as e:
                    print(f"Error saving image: {e}")         
            movie.append({
                    "date":formatted_date ,
                    "description":wp_content,
                    "name":namefilm,
                    "director": daodien,
                    "poster":image_pathposter,
                    "status":status,
                    "time": runtime,
                    "total_episode": 1,
                    "url_image":image_path,
                    "url_trailer": trailer_url,
                    "year": date.year,
                    "country_id":countryid,
                    "language":language,
                    "view" : random.randint(1000,1000000)

                })            
            idfilm+=1
            
           
            #lấy thông tin


driver.quit()          
movies = pd.DataFrame(movie)
movies.to_csv('movie.csv', index=False)
episodies = pd.DataFrame(episodie)
episodies.to_csv('episodie.csv', index=False)
detail_actors = pd.DataFrame(detail_actor)
print(actossssr)
detail_actors.to_csv('detail_actor.csv', index=False)
actossssrs = pd.DataFrame(actossssr)
actossssrs.to_csv('actor.csv', index=False)
genres = pd.DataFrame(genre)
genres.to_csv('genre.csv', index=False)
genredetails = pd.DataFrame(genredetail)
genredetails.to_csv('genredetails.csv', index=False)

countryss = pd.DataFrame(countrys)
countryss.to_csv('countrys.csv', index=False)