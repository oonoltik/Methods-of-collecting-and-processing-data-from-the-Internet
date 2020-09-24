import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    main_url = ['https://www.superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']


    def parse(self, response:HtmlResponse):

        #vacancies = response.css("div.vacancy-serp-item__row_header a.bloko-link::attr(href)").extract()

        vacancies  = response.css(
            'div.f-test-vacancy-item \
            a[class*=f-test-link][href^="/vakansii"]::attr(href)'
        ).extract()

        for vacancy in vacancies:
            yield response.follow(vacancy,callback=self.vacancy_parse)


        next_page = response.xpath('//span[text() = "Дальше"]/ancestor::a[@rel="next"]/@href').extract_first()
        # next_page = response.css( 'a[class="f-test-link-dalshe"]::attr(href)').extract_first()


        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1 ::text').extract_first()
        salary = response.css('div._3MVeX span[class="_3mfro _2Wp8I PlM3e _2JVkc"] ::text').extract()
        vacancy_link = response.url
        site_name = self.allowed_domains[0]




        yield JobparserItem(name=name, salary=salary, vacancy_link=vacancy_link, site_name=site_name)
        print()