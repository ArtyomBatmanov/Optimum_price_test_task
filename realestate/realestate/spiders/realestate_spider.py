import scrapy
from scrapy.http import HtmlResponse
import undetected_chromedriver as uc


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = [
        'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?place=0-6']

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = uc.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        html = self.driver.page_source

        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(html)

        response = HtmlResponse(url=self.driver.current_url, body=html, encoding='utf-8')

        for item in response.css('.NewBuildingItem__Wrapper-sc-o36w9y-0'):
            title = item.css('.NewBuildingItem__MainTitle-sc-o36w9y-6::text').get()
            address = item.css('.NewBuilding0Item__Text-sc-o36w9y-7::text').get()
            object_id = item.css('.NewBuildingItem__ObjectID-sc-o36w9y-8::text').get()
            yield {
                "title": title.strip() if title else None,
                "address": address.strip() if address else None,
                "object_id": object_id.strip() if object_id else None
            }

    def closed(self, reason):
        self.driver.quit()


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},
        },
    })
    process.crawl(MySpider)
    process.start()
