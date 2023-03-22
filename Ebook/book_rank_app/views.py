from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver

from trend_book_app.views import get_main_trends

try:
    import BeautifulSoup as bs
except:
    from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options

# Create your views here.

def homepage(request):
    # return HttpResponse('homepage')

    # trending
    trending_list = get_main_trends()


    naver_list = get_naver_rank()

    context = {
        'books': trending_list,
        'naver': naver_list
        # 'naver': []
    }

    return render(request, 'book_rank_app/base.html', context)
    # return render(request,'book_rank_app/base_hyejin.html')



def get_naver_rank():
    naver_list = []
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    naver_url = 'https://series.naver.com/ebook/top100List.series'
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(naver_url)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    base_url = 'https://series.naver.com'

    for i in range(10):
        row = int(i / 5 + 1)
        col = int(i % 5 + 1)
        # print(row, col)
        link_str = f"div#content > div > ul:nth-child({row}) > li:nth-child({col}) > a"
        rank = soup.select('li> span.num > em')[i].text.strip()
        image_src = soup.select('ul> li > a > img')[i]['src']
        title = soup.select('ul > li > a > strong')[i].text.strip()
        author = soup.select('ul > li > a > span.writer')[i].text.strip()
        # link = soup.select('div#content > div > ul > li > a')[i]['href']

        aaa = soup.select(link_str)
        link = soup.select(link_str)[0]['href']

        # content > div > ul:nth-child(1) > li:nth-child(2) > a
        # content > div > ul:nth-child(2) > li:nth-child(1) > a
        # content > div > ul:nth-child(2) > li:nth-child(3) > a

        book_detail = {
            'rank': rank,
            'image_src': image_src,
            'title': title,
            'author': author,
            'link': base_url+link,
        }

        naver_list.append(book_detail)

    return naver_list



# # 네이버 시리즈 랭킹
# def Naver_rank():
#     global naver_list
#
#     naver_list = []
#
#     options = webdriver.ChromeOptions()
#
#     # 창 열리지 않게
#     options.add_argument('headless')
#     naver_url = 'https://series.naver.com/ebook/top100List.series'
#
#     driver = webdriver.Chrome('chromedriver', options=options)
#     driver.get(naver_url)
#     html = driver.page_source
#     soup = bs(html, 'html.parser')
#
#     for i in range(10):
#         rank = soup.select('li> span.num > em')[i].text.strip()
#         image_src = soup.select('ul> li > a > img')[i]['src']
#         title = soup.select('ul > li > a > strong')[i].text.strip()
#         author = soup.select('ul > li > a > span.writer')[i].text.strip()
#         naver_list.append((rank, image_src, title, author))
#
#     return render('book_rank_app/base_hyejin.html',{"data": naver_list })


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

    return render('base_hyejin.html', {"data": yes24_list})
'''

# def post(request):
#     if request.method=="POST":
#         list=request.POST.getlist("data[]")
#         print(list)
#     return render('base_hyejin.html')
#
# def main():
#
#
#     while True:
#         Naver_rank()
#         # Yes24_rank()
#     # time.sleep(3600)
