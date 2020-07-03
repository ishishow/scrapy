# -*- coding: utf-8 -*-
import scrapy


class AtCosmeSpider(scrapy.Spider):
    name = "atcosme"
    print('@cosmeのレビューを検索します\nURLを入力してください')
    url = input('URL:')      # 検索キーワードの入力
    new_url = url.replace('top', 'reviews') 
    start_urls = [new_url]
    def parse(self, response):
        yield {
            'text': response.css("p.read::text").getall(),
            'star': response.css("p.reviewer-rating::text").get(),
            'date': response.css("p.mobile-date::text").get()
        }
        if response.css(".condition-limit-inner"):
            next_page_url = response.css("span.read-more>a::attr(href)").extract_first() 
        else:
            next_page_url = response.css("li.next>a::attr(href)").extract_first() 
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))