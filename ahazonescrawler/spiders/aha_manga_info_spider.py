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
            'ahazonescrawler.pipelines.AhaMangaInfoCrawlerStatusPipeline': 302
        },
        'IMAGES_STORE': './temp/manga/'
    }
    def start_requests(self):
        # Load crawling instructions.
        instructions = db_client.collection(self.root_collection).where(u'spider_name', u'==', self.name).where(u'crawling_status', u'==', u'new').stream()
        for inst in instructions:
            inst_dict = inst.to_dict()
            inst_dict['id'] = inst.id
            yield Request(url=inst_dict['source_url'], callback= self.parse_inst, cb_kwargs=dict(inst=inst_dict))

    def parse_inst(self, response, inst):
        loader = ItemLoader(item=AhaMangaInfoItem(), response=response)
        loader.add_value('manga_id', inst['manga_id'])
        loader.add_value('inst_id', inst['id'])
        if 'author_inst' in inst:
            self.add_inst(loader, 'author_inf', inst['author_inst'])
        if 'categories_inst' in inst:
            self.add_inst(loader, 'categories_inf', inst['categories_inst'])
        if 'summary_inst' in inst:
            self.add_inst(loader, 'summary_inf', inst['summary_inst'])
        if 'thumbnail_inst' in inst:
            self.add_inst(loader, 'thumbnail_url', inst['thumbnail_inst'])
        if 'preview_inst' in inst:
            self.add_inst(loader, 'preview_url', inst['preview_inst'])
        return loader.load_item()

    def add_inst(self, loader, item_attr, inst):
        if inst is None:
            return
        selector = inst['selector']
        path = inst['path']
        if selector == 'xpath':
            loader.add_xpath(item_attr, path)
        elif selector == 'css':
            loader.add_css(item_attr, path)
        else:
            self.logger.info(f'unsupported selector {selector}')
        return