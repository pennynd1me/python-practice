from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import math

serviceUrl = "https://m.land.naver.com/search/result/"
srcText = input("검색 장소를 입력하세요.")
url = serviceUrl + srcText

wd = webdriver.Chrome("chromedriver.exe")

# 창 최대화
wd.maximize_window()
wd.get(url)

time.sleep(2)

ele = wd.find_element_by_css_selector("#_countContainer > a.btn_option._complex")
ele.click()

wd.implicitly_wait(5)
howmany = wd.find_element_by_xpath('//*[@id="_listContainer"]/div/div[1]/a/h3/strong')
rangeNm = math.ceil(int(howmany.text)/20)
for i in range(rangeNm):
    eList = wd.find_elements_by_xpath('//*[@id="_listContainer"]/div/div[3]/div/div')
    action = ActionChains(wd)
    wd.implicitly_wait(5)
    time.sleep(1)
    action.move_to_element(eList[-1]).perform()
    time.sleep(1)
# 'SK뷰\n동별매물\n매매5억 3,000~12억 2,000\n전세3억 5,000~5억 8,000\n아파트1018세대총21동2008.11.07.\n79.5㎡ ~ 198.92㎡\n매매22 전세8 월세3'

jsonList = []
for j in range(len(eList)):
    json = eList[j].text
    splited = json.split("\n")
    splited.insert(0, j+1)
    print(splited)

a = input()