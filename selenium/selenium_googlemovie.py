from socket import AF_LINK
from bs4 import BeautifulSoup
from bs4.builder import TreeBuilder
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

url= ("https://play.google.com/store/movies/top")
# html = getRequestUrl(url)
# soup = BeautifulSoup(html, 'html.parser')

# with open("movie.html", "w", encoding="utf8") as f :
#     f.write(soup.prettify())

wd = webdriver.Chrome("chromedriver.exe")

# 창 최대화
wd.maximize_window()
wd.get(url)

# 화면 높이 만큼 스크롤 내리기
# wd.execute_script("window.scrollTo(0,1080)")

# 브라우저 높이 만큼 스크롤 내리기
# wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")

interval = 2 # 2초에 한번씩 스크롤 내리기
prev_height  = wd.execute_script("return document.body.scrollHeight")
while True :
    #스크롤 가장 아래로 내림
    wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    #페이지 대기
    time.sleep(interval)

    #스크롤 내린후 문서 높이
    curr_height  = wd.execute_script("return document.body.scrollHeight")

    if curr_height == prev_height :
        break
    prev_height = curr_height


print("스크롤 완료")

html = wd.page_source
soup = BeautifulSoup(html, "html.parser")
movies = soup.find_all("div", attrs={"class" : "Vpfmgd"})
print(f"영화갯수 : {len(movies)}")

movieList = []
for i,movie in enumerate(movies) : 
    title = movie.find("div" , attrs={"class" : "WsMG1c nnK0zc"}).get_text()
    price = movie.find("span" , attrs={"class" : "VfPpfd ZdBevf i5DZme"}).get_text()
    movieType = "" if None == movie.find("div" , attrs={"class" : "KoLSrc"}) else movie.find("div" , attrs={"class" : "KoLSrc"}).get_text()

    try :
        rank = movie.find("div" , attrs={"role" : "img"})["aria-label"]
        #rank = "4.3/5"
        mList = re.findall(r'([\d.]+)개',rank)
        rank = mList[1] + "/" + mList[0]
        rank2 = float(mList[1])
    except :
        rank = ""
        rank2 = 0
    

    link = movie.find("a" , attrs={"class" : "JC71ub"})["href"]
    movieList.append({"title":title, "price" : price, "movieType" : movieType, "rank" : rank, "rank2" : rank2, "link" : link})

sortMovies = sorted(movieList, key=lambda x:x['rank2'], reverse=True)
for i,movie in enumerate(sortMovies) : 
    print(f"번호 : {i+1}")
    print(f"제목 : "+ movie["title"])
    print(f"가격 : " + movie["price"])
    print(f"영화분류 :"+ movie["movieType"])
    print(f"평점 : "+ movie["rank"])
    print(f"링크 : https://play.google.com" + movie["link"])
    print("-"*100)

import json
with open(f"구글 영화 TOP {len(movies)} rank.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(sortMovies, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print(f"구글 영화 TOP {len(movies)} rank.json Saved" )