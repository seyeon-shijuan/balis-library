from django.shortcuts import render
from selenium import webdriver
import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options

# Create your views here.

def homepage(request):
    # return HttpResponse('homepage')

    # 1시간 단위 naver, yes24 함수 호출- 우선 naver 먼저 확인 후 yes24
    main()
    return render(request,'book_rank_app/base.html')

    


# 네이버 시리즈 랭킹
def Naver_rank():
    global naver_list

    naver_list = []

    options = webdriver.ChromeOptions()

    # 창 열리지 않게
    options.add_argument('headless')
    naver_url = 'https://series.naver.com/ebook/top100List.series'

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(naver_url)
    html = driver.page_source
    soup = bs(html, 'html.parser')

    for i in range(10):
        rank = soup.select('li> span.num > em')[i].text.strip()
        image_src = soup.select('ul> li > a > img')[i]['src']
        title = soup.select('ul > li > a > strong')[i].text.strip()
        author = soup.select('ul > li > a > span.writer')[i].text.strip()
        naver_list.append((rank, image_src, title, author))

    return render('book_rank_app/base.html',{"data": naver_list })


'''
naver 먼저 완성 후 추가
#Yes24 랭킹

def Yes24_rank():

    global yes24_list

    yes24_list = []

    options = webdriver.ChromeOptions()

    # 창 열리지 않게
    options.add_argument('headless')
    yes24_url = 'http://www.yes24.com/Mall/Main/EBook/017?CategoryNumber=017'

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(yes24_url)
    html = driver.page_source
    soup = bs(html, 'html.parser')
   
    for i in range(10):
        rank = soup.select('div.item_img > div > span > span > em')[i].text.strip()
        image_src = soup.select('div.item_img > div > span > span > a > em.img_bdr > img')[i]['data-original']
        title = soup.select('ul > li > div > div > div.info_row.info_name > a')[i].text.strip()
        author = soup.select('ul > li > div > div.item_info > div.info_row.info_pubGrp > span.info_auth')[i].text.strip()

        yes24_list.append((rank, image_src, title, author))

    return render('base.html', {"data": yes24_list})
'''

def post(request):
    if request.method=="POST":
        list=request.POST.getlist("data[]")
        print(list)
    return render('base.html')

def main():
    
  
    while True:
        Naver_rank()
        # Yes24_rank()
    time.sleep(3600)
