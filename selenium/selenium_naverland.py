from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
from datetime import datetime
import math
import re
import json

serviceUrl = "https://m.land.naver.com/search/result/"
srcText = input("검색 장소를 입력하세요.")
url = serviceUrl + srcText

wd = webdriver.Chrome("chromedriver.exe")

# 창 최대화
wd.implicitly_wait(10)
wd.maximize_window()
wd.get(url)
time.sleep(2)
# https://m.land.naver.com/cluster/ajax/articleList?&rletTpCd=APT&tradTpCd=A1%3AB1%3AB2&cortarNo=4111300000&page=1
# https://m.land.naver.com/cluster/ajax/complexList?&rletTpCd=APT&tradTpCd=A1%3AB1%3AB2&cortarNo=4111300000&page=1
html = wd.page_source
bs = BeautifulSoup(html, 'html.parser')
jssource = bs.select_one('#mapSearch > script')
cortarNo = re.search(r'cortarNo: \'(\d*)\'', jssource.string).group(1)

pageNm = 1
resultList = []
while True :
    complexurl = f"https://m.land.naver.com/cluster/ajax/complexList?&rletTpCd=APT&tradTpCd=A1%3AB1%3AB2&cortarNo={cortarNo}&page={pageNm}"
    wd.execute_script(f'window.open("{complexurl}","_blank");')
    wd.switch_to.window(wd.window_handles[1])
    html = wd.page_source
    html = html[84:-20]
    json_dict = json.loads(html)
    pageNm += 1
    time.sleep(0.3)
    wd.close()
    resultList.append(json_dict)
    wd.switch_to.window(wd.window_handles[0])
    if json_dict['more'] == False:
        break

with open(f"naver_land_{srcText.replace(' ', '_')}_complex.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print(f"naver_land_{srcText.replace(' ', '_')}_complex.json Saved" )

pageNm = 1
resultList = []
while True :
    articleurl = f"https://m.land.naver.com/cluster/ajax/articleList?&rletTpCd=APT&tradTpCd=A1%3AB1%3AB2&cortarNo={cortarNo}&page={pageNm}"
    wd.execute_script(f'window.open("{articleurl}","_blank");')
    wd.switch_to.window(wd.window_handles[1])
    html = wd.page_source
    html = html[84:-20]
    json_dict = json.loads(html)
    pageNm += 1
    time.sleep(0.3)
    wd.close()
    resultList.append(json_dict)
    wd.switch_to.window(wd.window_handles[0])
    if json_dict['more'] == False:
        break

with open(f"naver_land_{srcText.replace(' ', '_')}_article.json", "w", encoding="utf8") as outfile :
    retJson = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(retJson)
print(f"naver_land_{srcText.replace(' ', '_')}_article.json Saved" )


a = input()