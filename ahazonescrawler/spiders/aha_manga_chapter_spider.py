import datetime
from scrapy import Spider, Request
from scrapy.selector.unified import Selector
from scrapy.http.response.html import HtmlResponse
from ahazonescrawler.firebase.admin import db_client
from ahazonescrawler.items import AhaMangaChaptersItem
from ahazonescrawler.utilities import extract_chapter_num

class AhaMangaChapterSpider(Spider):
    name = 'aha-manga-chapter-spider'
    root_collection = 'aha_crawler'
    custom_settings = {
        'ITEM_PIPELINES': {
            'ahazonescrawler.pipelines.AhaMangaChapterDataPipeline': 300,
            'ahazonescrawler.pipelines.AhaMangaChapterCrawlerStatusPipeline': 305,
        }
    }

    def start_requests(self):
        now = datetime.datetime.utcnow()
        # Load crawling instructions.
        instructions = db_client.collection(self.root_collection).where(u'spider_name', u'==', self.name).where(u'next_time', u'<=', now).where(u'last_success', u'==', True).stream()
        for inst in instructions:
            inst_dict = inst.to_dict()
            inst_dict['id'] = inst.id
            yield Request(url=inst_dict['source_url'], callback= self.parse_inst, cb_kwargs=dict(inst=inst_dict))

    def parse_inst(self, response, inst):
        item = AhaMangaChaptersItem()
        item['inst_id'] = inst.get('id', None)
        item['manga_id'] = inst.get('manga_id', None)
        item['lang_version'] = inst.get('lang_version', None)
        item['cron_time'] = inst.get('cron_time', None)
        item['source_id'] = inst.get('source_id', '1')
        item['chapters'] = list()

        last_chapter = inst.get('last_chapter', -1)
        last_chapter_id = last_chapter
        last_chapter_url = None
        link_list = self.get_element(response, inst.get('list_inst', None), False)
        for link in link_list:
            url = self.get_element(link, inst.get('url_inst', None))
            id = self.get_num(self.get_element(link, inst.get('id_inst', None)))
            if url and id > last_chapter:
                item['chapters'].append({
                    u'chapter_id': id,
                    u'chapter_url': response.urljoin(url)
                })
                if id > last_chapter_id:
                    last_chapter_id = id
                    last_chapter_url = url
        if last_chapter_url:
            yield Request(url=last_chapter_url, callback= self.validate_last, cb_kwargs=dict(item=item))

    def validate_last(self, response, item):
        num = self.count_images(response)
        if num > 3:
            return item

    def count_images(self, response):
        return len(response.xpath('//img/@src'))

    def get_element(self, parent, inst, text = True):
        if inst is None:
            return
        if not isinstance(parent, (Selector, HtmlResponse)):
            return parent
        selector = inst.get('selector', None)
        path = inst.get('path', None)
        if selector == 'xpath':
            if text:
                return parent.xpath(path).get()
            else:
                return parent.xpath(path)
        elif selector == 'css':
            if text:
                return parent.css(path).get()
            else:
                return parent.css(path)
        else:
            self.logger.warn(f'unsupported selector {selector}')
    def get_num(self, num_in_str):
        n = extract_chapter_num(num_in_str)
        if n is None:
            self.logger.error(f'cannot get chapter number from {num_in_str}')
            return None
        return n