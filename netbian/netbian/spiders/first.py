import scrapy
from scrapy import Request
from netbian.items import NetbianItem


class FirstSpider(scrapy.Spider):
    name = 'first'
    # allowed_domains = ['https://pic.netbian.com/index.html']
    domains = 'https://pic.netbian.com'
    start_urls = ['https://pic.netbian.com/index.html/']
    base_url = 'https://pic.netbian.com/index_{}.html'
    max_page = 10  # 最多爬取10页数据
    path_index = 2

    def start_requests(self):
        for i in range(self.path_index, self.max_page):
            url = self.base_url.format(i)
            yield Request(url=url, callback=self.parse)
            print('爬取完第 %s 页' % i)

    # 解析页面列表
    def parse(self, response):
        sel = response.css("div.slist ul.clearfix")

        for li in sel.xpath(".//li"):
            link_image = self.domains + li.xpath("./a/@href").extract_first()
            image_name = li.xpath("./a/@title | ./a/img/@alt").extract_first()
            print(image_name)

            item = NetbianItem()
            item['image_name'] = image_name
            headers = {'referer': link_image}
            yield Request(link_image, callback=self.parse_img, meta={'item': item}, headers=headers)

    # 解析页面里面

    def parse_img(self, response):
        item = response.meta['item']
        image_src = self.domains + \
            response.xpath('//*[@id="img"]/img/@src').extract_first()
        item['image_src'] = image_src

        yield item
