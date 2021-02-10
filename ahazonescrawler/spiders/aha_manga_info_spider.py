from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ahazonescrawler.firebase.admin import db_client
from ahazonescrawler.items import AhaMangaInfoItem

class AhaMangaInfoSpider(Spider):
    name = 'aha-manga-info-spider'
    root_collection = 'aha_crawler'
    custom_settings = {
        'ITEM_PIPELINES': {
            'ahazonescrawler.pipelines.AhaMangaInfoThumbnailPipeline': 300,
            'ahazonescrawler.pipelines.AhaMangaInfoDataPipeline': 301,
        },
    }
    def start_requests(self):
        # Load crawling instructions.
        instructions = db_client.collection(self.root_collection).where(u'spider_name', u'==', self.name).where(u'crawling_status', u'==', u'new').stream()
        for inst in instructions:
            yield Request(url=inst['source_url'], callback= self.parse_inst, cb_kwargs=dict(inst=inst))
    def parse_inst(self, response, inst):
        loader = ItemLoader(item=AhaMangaInfoItem(), response=response)
        loader.add_value('manga_id', inst['manga_id'])
        self.load_item(loader, 'author_inf', inst['author_inst'])
        self.load_item(loader, 'categories_inf', inst['categories_inst'])
        self.load_item(loader, 'summary_inf', inst['summary_inst'])
        self.load_item(loader, 'thumbnail_url', inst['thumbnail_inst'])
        return loader.load_item()

    def load_item(self, loader, item_attr, inst):
        if inst is None:
            return
        selector = inst['author_inst']['selector']
        path = inst['author_inst']['path']
        if selector == 'xpath':
            loader.add_xpath(item_attr, path)
        elif selector == 'css':
            loader.add_css(item_attr, path)
        else:
            self.logger.info(f'unsupported selector {selector}')
        return