# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class NetbianPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_src'])

    def file_path(self, request, response=None, info=None, *, item=None):
        return item['image_name']+'.jpg'

    def item_completed(self, results, item, info):
        '传递给下一个，如果你还有一个piple的话'
        return item
