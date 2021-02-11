# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import ntpath
import logging
from urllib.parse import urljoin
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from ahazonescrawler.firebase.admin import db_client, storage_client

logger = logging.getLogger(__name__)

def get_str(value, delimiter=''):
    if type(value) is list:
        return delimiter.join(str(e) for e in value)
    return value

def get_list(value, delimiter=','):
    if type(value) is str:
        return value.split(delimiter)
    return value

class AhazonescrawlerPipeline:
    def process_item(self, item, spider):
        return item

# This pipeline to use insert manga info into firestore
class AhaMangaInfoDataPipeline:
    root_collection = 'aha_manga'

    def open_spider(self, spider):
        logger.info('Start inserting manga info data')

    def close_spider(self, spider):
        logger.info('Stop inserting manga info data')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        manga_id = get_str(adapter['manga_id'])
        if manga_id is None:
            raise DropItem('the manga_id is none')
        # save info to firestore.
        author = get_str(adapter['author_inf'])
        categories = get_list(adapter['categories_inf'])
        summary = get_str(adapter['summary_inf'], delimiter=' ')
        db_client.collection(self.root_collection).document(manga_id).set({
            u'author': author,
            u'categories': categories,
            u'summary': summary
        }, merge=True)
        # return item to the next pipeline.
        return item

#
class AhaMangaInfoThumbnailPipeline(ImagesPipeline):
    root_collection = 'aha_manga'

    def get_media_requests(self, item, info):
        url = get_str(item['thumbnail_url'])
        if url:
            yield Request(urljoin('http://', url))
        else:
            logger.error('the thumbnail_url is none')

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('item contains no images')
        # - Save to storage.
        manga_id = get_str(adapter['manga_id'])
        if manga_id is None:
            raise DropItem('the manga_id is none')
        file_name = self.path_leaf(image_paths[1])
        blob = storage_client.blob(f'{manga_id}/{file_name}')
        blob.upload_from_filename(image_paths[1])
        # - Save the download url to firestore.
        db_client.collection(self.root_collection).document(manga_id).set({
            u'thumbnail_url': blob.media_link
        }, merge=True)
        return item

    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

class AhaMangaInfoCrawlerStatusPipeline:
    root_collection = 'aha_crawler'
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        inst_id = get_str(adapter['inst_id'])
        if inst_id:
            db_client.collection(self.root_collection).document(inst_id).set({
                u'crawling_status': 'done'
            }, merge=True)
        else:
            logger.error('the inst_id is none')