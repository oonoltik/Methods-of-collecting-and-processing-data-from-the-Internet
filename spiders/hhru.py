import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response:HtmlResponse):
        vacancies = response.css("div.vacancy-serp-item__row_header a.bloko-link::attr(href)").extract()
        for vacancy in vacancies:
            yield response.follow(vacancy,callback=self.vacancy_parse)

        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//text()").extract()
        vacancy_link = response.url
        site_name = self.allowed_domains[0]

        yield JobparserItem(name=name, salary=salary, vacancy_link=vacancy_link, site_name=site_name )
        print()