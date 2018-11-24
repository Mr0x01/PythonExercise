import scrapy,time,logging
from renrenspider.items import *

class Downloader(scrapy.Spider):
    name = "renrendownloader"
    custom_settings = {
        'ITEM_PIPELINES':{
            'renrenspider.pipelines.RenrendownloadPipeline':400
        }
    }
    def start_requests(self):
        if RenrenspiderModel.table_exists() == False:
           RenrenspiderModel.create_table()
        return [scrapy.Request(
                url="http://3g.renren.com",
                callback=self.download,
            )] 
    
    def download(self,response):
        
        while True:
                img_model = RenrenspiderModel.get_or_none(RenrenspiderModel.status == "0")
                if img_model != None:
                    item = RenrenspiderItem()
                    item["img_id"] = img_model.img_id
                    item["friend_name"] = img_model.friend_name
                    item["album_name"] = img_model.album_name
                    item["img_date"] = img_model.img_date
                    item["img_comment"] = img_model.img_comment
                    item["img_url"] = img_model.img_url
                    item["img_path"] = img_model.img_path
                    RenrenspiderModel.update(status='1').where(RenrenspiderModel.img_id == img_model.img_id).execute()
                    yield item
                else:
                    logging.warning("暂无任务，等待10秒")
                    time.sleep(10)