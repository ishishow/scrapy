# -*- coding: utf-8 -*-
import scrapy


class AmazonJapanSpider(scrapy.Spider):
    name = "AmazonJapan"
    print('Amazonのレビューを検索します\nURLを入力してください')
    url = input('URL:')      # 検索キーワードの入力
    new_url = url.replace('dp', 'product-reviews') 
    start_urls = [new_url]

    def parse(self, response):
        for info in response.cee(".review>.a-row>.cellwidget"):
            star_all = info.css(".a-icon-star::text").get()
            date_all = info.css(".review-date::text").get()
            yield {
                'text': info.css(".review-text-content>span::text").getall(),
                'star': star_all[-3:],
                'date': date_all[0:10]
            }

        next_page_url = response.css("li.a-last>a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))