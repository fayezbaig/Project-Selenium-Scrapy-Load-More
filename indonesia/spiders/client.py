import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


class ClientSpider(scrapy.Spider):
    name = "client"
    allowed_domains = ["www.airalo.com"]
    start_urls = ["https://www.airalo.com/"]

    def parse(self, response):

        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome()
        driver.get(response.url) 

        time.sleep(10)

        load_more = driver.find_element(by=By.CLASS_NAME, value='show-all-btn.btn-primary-hv')

        time.sleep(5)

        load_more.click()
        
        time.sleep(10)

        page_source=driver.page_source

        driver.quit()

        response = scrapy.http.HtmlResponse(url=response.url, body=page_source, encoding='utf-8')

        country_list = response.css('div.store-countries-and-regions-list.d-grid.gap-10.gap-sm-30.store-grid-cols-1.store-grid-cols-sm-2.store-grid-cols-md-3.store-grid-cols-lg-4 div.store-item.aloo')

        for country in country_list:

            url = country.css('a::attr(href)').get()

            yield response.follow(url,callback=self.parse_details)

    def parse_details(self, response):

        country_cards = response.css('div.d-grid.gap-30.store-grid-cols-1.store-grid-cols-sm-2.store-grid-cols-md-3.package-list a.sim-item-link')

        for country_card in country_cards:


            yield {
                'company' : 'airflow',
                'coverage' : country_card.css('p.value.sim-item-row-right-value::text').extract()[0].strip(),
                'data' : country_card.css('p.value.sim-item-row-right-value::text').extract()[1].strip(),
                'validity' : country_card.css('p.value.sim-item-row-right-value::text').extract()[2].strip(),
                'price' : country_card.css('p.value.sim-item-row-right-value::text').extract()[3].strip(),
                # 'url' : country_card.css('a::attr(href)').get(),
                'url': response.url
               }
            
