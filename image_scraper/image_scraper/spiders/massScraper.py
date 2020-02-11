from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from image_scraper.items import ImageItem


class FaceSpider(CrawlSpider):
    name = "img_scraper"
    allowed_domains = ["thewondrous.com"]
    start_urls = ["https://thewondrous.com/top-55-most-beautiful-hollywood-babes/"]
    
    def parse(self, response):
        image = ImageItem()
        image['title'] = response.xpath('//strong/text()').extract()
        image['image_urls'] = response.xpath("//p/a/img/@data-lazy-src").extract()
        # image['image_urls'] = response.xpath("//img[@class='alignnone']/@src").extract()
        
        # print image
        return image
        