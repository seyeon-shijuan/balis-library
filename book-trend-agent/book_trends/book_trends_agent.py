# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
from typing import Tuple
from crawler.base_crawler import BaseCrawler
import pandas as pd
import datetime as dt
from dateutil.tz import gettz


class BestBooksCrawler:
    def __init__(self, url: str, option: Options):
        self.bookstore_crawler = BaseCrawler(url, option=option)
        self.bookstore_crawler.open_browser()

    def _naver_base_info(self, j, header, base_url, isbn_selector):
        # if j == 19:
        #     a = 5

        # 기본 정보
        rank = header.select("em")[0].text
        title = header.select("strong")[0].text
        writer = header.select("span.writer")[0].text.split(',')[0]
        image = header.select("img")[0]['src']
        sub_link = header.select("a")[0]['href']
        container_selector = 'div#book_section-info > div.bookBasicInfo_basic_info__HCWyr > ul'

        # 책 상세정보페이지 (to get isbn link)
        isbn_link = self.bookstore_crawler.quick_attr_in_link(base_url + sub_link, isbn_selector, 'href')

        # 책 상세 정보가 없는 경우 -> 국립중앙도서관 전자책 ISBN 조회
        if not isbn_link:
            title_tmp = title.replace(' ', '+')
            gov_url = f'https://www.nl.go.kr/seoji/contents/S80100000000.do?page=1&pageUnit=10&schType=simple&schFld=title&schStr={title_tmp}&ebookYn=Y'

            gov_sel = 'div#resultList_div'
            gov_tag = self.bookstore_crawler.quick_tag_in_link(gov_url, gov_sel)

            try:
                # 검색 결과가 없는 경우(ISBN 번호가 부여되지 않은 전자책의 경우)
                isbn_container = gov_tag.find('li', string='제본형태: 전자책').find_parent()
            except AttributeError:
                print(f"rank {rank} : {title} - does not exist in gov-library")
                return None

            gov_isbn_tag = isbn_container.select("li:nth-child(3)")
            tmp = gov_isbn_tag[0]
            isbn_val = tmp.text

            # ISBN: 978-89-378-3637-4 (05830)
            isbn_val = isbn_val.split(' ')[1].replace('-', '')
            print(f'naver {rank}위 {title} 수집 필요')

        else:
            # isbn 추출 (parent select)
            self.bookstore_crawler.new_tab(isbn_link)

            soup = self.bookstore_crawler.get_soup()

            try:
                # 성인인증 페이지인경우 IndexError
                container = soup.select(container_selector)[0]
            except IndexError:
                print(f"rank {rank} : {title} - unable to collect due to rate-18")
                return None

            isbn_container = container.find('div', string='ISBN').find_parent()
            isbn_tag = isbn_container.select("div:nth-child(2)")
            isbn_val = isbn_tag[0].text
            self.bookstore_crawler.to_preveious_tap()

        # isbn, 순위, 사이트, 제목, 작가, 이미지 수집
        return {
            'isbn': isbn_val,
            'rank': rank,
            'website': 'naver',
            'title': title,
            'writer': writer,
            'image': image
        }

    def fetch_naver_best(self):
        target = 'https://series.naver.com/ebook/top100List.series?page='
        wrapper = 'div#content > div.lst_thum_wrap'
        base_url = 'https://series.naver.com'
        isbn_selector = '#content > ul.end_info.NE\=a\:ebi > li:nth-child(2) > span > a'
        page_books = []

        for i in range(1, 6):
            # page_books = []
            self.bookstore_crawler.move_page(target+str(i))
            ori_element = self.bookstore_crawler.select_element(selector=wrapper)[0]
            headers = ori_element.find_all("li", class_=None)

            for j, header in enumerate(headers):
                rst = self._naver_base_info(j, header, base_url, isbn_selector)
                if rst:
                    page_books.append(rst)
                time.sleep(0.5)

        return page_books

    def _millie_base_info(self, j, header):
        # isbn_wrapper = 'div#wrap > section > div > div.book-content > div:nth-child(7) > div.introduction.section > div.book-info-detail.slide-container'
        isbn_wrapper = 'div.book-info-detail.slide-container'
        # 기본 정보
        rank = header.select("div.book_ranking")[0].text
        title = header.select("p.book_name")[0].text
        writer = header.select("p.book_writer")[0].text
        image = header.select("img")[0]['src']
        sub_link = header.select("a")[0]['href']
        millie_id = sub_link.split('seq=')[1]

        # 책 상세정보페이지 (to get isbn link)
        base_url = f'https://www.millie.co.kr/v3/bookdetail/{millie_id}?nav_hidden=y'

        # isbn 추출 (parent select)
        self.bookstore_crawler.new_tab(base_url)
        soup = self.bookstore_crawler.get_soup()
        container = soup.select(isbn_wrapper)[0]

        try:
            # ISBN이 없는 경우 AttributeError
            isbn_container = container.find('p', string='ISBN').find_parent()
        except AttributeError:
            return None

        isbn_tag = isbn_container.select("strong")
        isbn_val = isbn_tag[0].text
        self.bookstore_crawler.to_preveious_tap()

        # isbn, 순위, 사이트, 제목, 작가, 이미지 수집
        return {
            'isbn': isbn_val,
            'rank': rank,
            'website': 'millie',
            'title': title,
            'writer': writer,
            'image': image
        }

    def fetch_millie_best(self):
        wrapper = 'div#bookList'
        page_books = []

        ori_element = self.bookstore_crawler.select_element(selector=wrapper)[0]
        headers = ori_element.find_all("li", class_=None)
        for j, header in enumerate(headers):
            rst = self._millie_base_info(j, header)
            print(rst)

            if rst:
                page_books.append(rst)

            time.sleep(0.5)

        return page_books

    def export_to_csv(self, in_list, outfile):
        df = pd.DataFrame.from_records(in_list)
        today = dt.datetime.now(gettz('Asia/Seoul')).today().strftime('%Y-%m-%d')
        df['date'] = today
        df = df.drop_duplicates(subset='isbn', keep='first')
        df.to_csv(f'../outfile/rank/{outfile}_{today}.csv', mode='w', index=False, header=True, encoding='utf-8-sig')
        print(outfile+' is saved')


def main():

    # setup
    option = Options()
    option.add_argument("disable-infobars")
    option.add_argument("disable-extensions")
    # option.add_argument("start-maximized")
    option.add_argument('disable-gpu')
    # option.add_argument('headless')

    # crawler = BestBooksCrawler('https://series.naver.com/ebook/home.series', option)


    # 1. 판매량
    # 1-1a) 네이버 베스트 100 목록 수집
    # naver_list = crawler.fetch_naver_best()

    # 1-1b) 네이버 CSV 파일로 쓰기
    # crawler.export_to_csv(naver_list, 'naver')

    # 1-2a) 밀리의 서재 베스트 100 목록 수집
    # crawler.bookstore_crawler.quit_browser()
    # crawler.bookstore_crawler.new_browser('https://www.millie.co.kr/viewfinder/more_milliebest.html?range=week&referrer=best', option)
    millie_link = 'https://www.millie.co.kr/viewfinder/more_milliebest.html?range=week&referrer=best'

    crawler = BestBooksCrawler(millie_link, option)
    millie_list = crawler.fetch_millie_best()

    # 1-2b) 밀리의 서재 CSV 파일로 쓰기
    crawler.export_to_csv(millie_list, 'millie')

    a = 0




    
    # 1-2) CSV DB로 적재
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


