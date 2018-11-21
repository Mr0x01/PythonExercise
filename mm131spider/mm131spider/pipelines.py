# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Mm131SpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['ImgUrl']:
            yield Request(image_url, headers={"Referer": item["ImgReferer"]}, meta={
                'item': item['ImgName']
            })

    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_id = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(name, image_id)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['ImgPath'] = image_path
        return item
