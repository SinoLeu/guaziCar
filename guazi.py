import requests
from lxml import etree
import time


class guazi(object):
    def __init__(self, city, brand='buy', price=None, ):
        print(city, brand, price)
        self.url = 'https://www.guazi.com'
        self.city = city
        self.brand = brand
        self.price = price
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }

    def _get_url(self, page=1):
        # print('get url')
        return self.url + '/' + str(self.city) + '/' + str(self.brand) + '/' + (
            'o' + str(page) + str(self.price) + '/' if self.price else 'o' + str(page))

    def _get_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            # print(response.text)
            if response.status_code == 200:
                return response.text
        except:
            print('get page error!')

    def _parse_page(self, html):
        doc = etree.HTML(html)
        li = doc.xpath(
            "/html/body[@class='list']/div[@class='list-wrap js-post']/ul[@class='carlist clearfix js-top']/li/a[@class='car-a']")
        # car = li[0].xpath('/img')
        # print(type(li))
        # print(li)
        for item in li:
            print('-------------------')
            print('detail_url: ', self.url + item.xpath('./@href')[0])
            print('image_url:', item.xpath('./img/@src')[0])
            print('name:', item.xpath('./div[@class="t"]')[0].text)
            print('yearAndfar:', item.xpath('string(./div[@class="t-i"])'))
            print('price:', item.xpath('string(./div[@class="t-price"]/p)'))
            print('-------------------')

    def _get_max_page(self):
        html = self._get_page(self._get_url())
        # print(html)
        # print(html)
        doc = etree.HTML(html)
        pagelink = doc.xpath(
            "string(/html/body[@class='list']/div[@class='list-wrap js-post']/div[@class='pageBox']/ul[@class='pageLink clearfix']/li[last()-1])")
        # print(type(pagelink))
        return pagelink

    def spider(self):
        # print(self._get_max_page())
        max_page = self._get_max_page()
        max_page = int(max_page) if max_page else 1
        print('有{}页数据待抓取'.format(max_page))
        for page in range(1, max_page + 1):
            _url = self._get_url(page)
            print(_url)
            html = self._get_page(_url)
            self._parse_page(html)
            time.sleep(3)


g = guazi('gz', 'bmw-7', 'p18')
g.spider()
