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


class RenrenspiderPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item
    def get_media_requests(self, item, info):
        yield Request(
            url=item['img_url'],
            headers={
                "user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
            },
            meta={
                "friend_name": item["friend_name"],
                "img_comment": item["img_comment"],
                "img_date": item["img_date"],
                "album_name": item["album_name"]
            })

    def file_path(self, request, response=None, info=None):
        name = request.meta['img_comment'] + \
            "#" + str(request.meta['img_date']) + "#" + str(uuid.uuid4()).replace("-","")
        name = re.sub(r'[:]', "：", name)
        name = re.sub(r'[?\\*|\"<>/()]', '', name)[:100]
        friend_name = request.meta['friend_name']
        friend_name = re.sub(r'[:]', "：", friend_name)
        friend_name = re.sub(r'[?\\*|\"<>/()]', '', friend_name)[:100]
        album_name = request.meta['album_name']
        album_name = re.sub(r'[:]', "：", album_name)
        album_name = re.sub(r'[?\\*|\"<>/()]', '', album_name)[:100]
        filename = u'full/{0}/{1}/{2}.jpg'.format(
            friend_name, album_name, name)
        return filename

    # def item_completed(self, results, item, info):
    #     image_path = [x['path'] for ok, x in results if ok]
    #     if not image_path:
    #         raise DropItem('Item contains no images')
    #     item['img_path'] = image_path
    #     return item
