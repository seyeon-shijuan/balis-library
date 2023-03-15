from crawler.bookstore_crawler import NaverSeriesCrawler


def test_agent():
    target = 'https://series.naver.com/ebook/detail.series?productNo=9521460'
    ns_crawler = NaverSeriesCrawler(target)
    ns_crawler.bookstore_crawler.open_browser()

    img_selector = '#container > div.aside.NE\=a\:ebi > a > img'

    image = ns_crawler.bookstore_crawler.get_attr(selector=img_selector, attr='src')

    a = 0





if __name__ == '__main__':
    test_agent()