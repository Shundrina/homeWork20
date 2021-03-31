from scrapy import Spider, Request

from homeWork20.items import PeopleItem


class WorkuaSpider(Spider):
    name = 'workua'
    allowed_domains = ['work.ua']
    start_urls = [
        'https://www.work.ua/resumes-kharkiv/',
    ]

    site_url = 'https://work.ua'

    def parse(self, response):

        for person in response.css('div.card.resume-link'):
            name = person.css('div > b::text').get()
            old = person.css('div > span:nth-child(3)::text').get()
            position = person.css('h2 > a::text').get()

            people_item = PeopleItem()
            people_item['name'] = name.strip()
            people_item['old'] = int(old) if old.strip().isdigit() else None
            people_item['position'] = position

            detail_page_uri = person.css('div.row div a::attr(href)').get()
            detail_page_url = self.site_url + detail_page_uri
            yield Request(detail_page_url, self.parse_detail_page, meta={
                'people_item': people_item,
            })

        next_page_uri = response.css(
            'ul.pagination-small li a::attr(href)').getall()
        if next_page_uri:
            next_page_url = self.site_url + next_page_uri[-1]
            yield Request(next_page_url)

    def parse_detail_page(self, response):
        detail_info = response.css('p#addInfo::text').get()
        people_item = response.meta['people_item']
        people_item['detail_info'] = detail_info
        yield people_item
