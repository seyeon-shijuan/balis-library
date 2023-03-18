from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from typing import Tuple
from crawler.base_crawler import BaseCrawler
import pandas as pd


class BestBooksCrawler:
    def __init__(self, url: str, option: Options):
        self.bookstore_crawler = BaseCrawler(url, option=option)
        self.bookstore_crawler.open_browser()

    def get_naver_best(self):
        target = 'https://series.naver.com/ebook/top100List.series?page='
        wrapper = 'div#content > div.lst_thum_wrap'
        base_url = 'https://series.naver.com'
        isbn_selector = '#content > ul.end_info.NE\=a\:ebi > li:nth-child(2) > span > a'

        for i in range(1, 6):
            page_books = []
            self.bookstore_crawler.move_page(target+str(i))
            ori_element = self.bookstore_crawler.select_element(selector=wrapper)[0]
            headers = ori_element.find_all("li", class_=None)

            for header in headers:
                rank = header.select("em")[0].text
                title = header.select("strong")[0].text
                writer = header.select("span.writer")[0].text
                image = header.select("img")[0]['src']
                sub_link = header.select("a")[0]['href']

                isbn_link = self.bookstore_crawler.quick_select_in_link(base_url+sub_link, isbn_selector, 'href')
                a = 1
                # self.bookstore_crawler.quit_browser(isbn_link,)

                detail_dict = {'rank': rank, 'title': title, 'writer': writer, 'image': image,}
                yield

                # yield (header, list(get_content(header.nextSibling)))


            a = 0




            # 사이트, 순위, 제목, 작가, 이미지 수집

            # isbn 수집





        return 0



def main():

    # setup
    option = Options()
    option.add_argument("disable-infobars")
    option.add_argument("disable-extensions")
    # option.add_argument("start-maximized")
    option.add_argument('disable-gpu')
    # option.add_argument('headless')

    crawler = BestBooksCrawler('https://series.naver.com/ebook/home.series', option)


    # 1. 판매량
    # 1-1) 네이버, 교보, Yes24, 밀리의 서재, 리디북스 베스트 100 목록 수집
    naver_df = crawler.get_naver_best()
    a =0


    # # 새 브라우저
    # crawler.bookstore_crawler.quit_browser()
    # crawler.bookstore_crawler.new_browser('https://www.naver.com/', option)







    
    # 1-2) CSV 추출 및 DB로 적재
    # isbn / title / website / sales_rank / interest(관심도) /

    # 2. 관심도
    # 2-1) 트위터 최근 7일내 해당 도서 언급량 수집

    # 2-2) CSV 추출 및 DB로 적재
    # title / text / created_at / retweet_count / favorite_count

    # 2-3) 네이버 리뷰 수집

    # 2-4) CSV 추출 및 DB로 적재
    # title / text / created_at

    # 3. 점수 계산
    # Distinct Value Filter 하여 DB의 score table 에 Insert
    # 관심량 : 트윗 count x 1로 normalize + 네이버 리뷰 count x 1로 normalize
    # 판매량 : 도서의 각 사이트별 순위를 모두 더한 뒤 x 1로 normalize
    # 총 점수 : 관심량 x 0.6 + 판매량 x 0.4로 계산

    # 3-1)




if __name__ == '__main__':
    main()


