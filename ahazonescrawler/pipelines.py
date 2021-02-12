# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import ntpath
import logging
import croniter
import datetime
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

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        manga_id = get_str(adapter['manga_id'])
        if manga_id is None:
            raise DropItem('the manga_id is none')
        # save info to firestore.
        author = get_str(adapter['author_inf']) if 'author_inf' in adapter else None
        categories = get_list(adapter['categories_inf']) if 'categories_inf' in adapter else None
        summary = get_str(adapter['summary_inf'], delimiter=' ') if 'summary_inf' in adapter else None
        doc = {}
        if author:
            doc['author'] = author
        if categories:
            doc['categories'] = categories
        if summary:
            doc['summary'] = summary
        if doc:
            db_client.collection(self.root_collection).document(manga_id).set(doc, merge=True)
        # return item to the next pipeline.
        return item

#
class AhaMangaInfoThumbnailPipeline(ImagesPipeline):
    root_collection = 'aha_manga'
    is_thumbnail = False
    is_preview = False

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        thumbnail_url = get_str(adapter['thumbnail_url']) if 'thumbnail_url' in adapter else None
        if thumbnail_url:
            self.is_thumbnail = True
            yield Request(urljoin('http://', thumbnail_url))
        else:
            logger.error('the thumbnail_url is none')
        preview_url = get_str(adapter['preview_url']) if 'preview_url' in adapter else None
        if preview_url:
            self.is_preview = True
            yield Request(urljoin('http://', preview_url))
        else:
            logger.error('the preview_url is none')

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)
        manga_id = get_str(adapter['manga_id'])
        if manga_id is None:
            raise DropItem('the manga_id is none')

        thumbnail = None
        preview = None
        if self.is_thumbnail:
            ok, x = results[0]
            if ok and x['path']:
                thumbnail = x['path']
        if self.is_preview:
            ok, x = results[1] if len(results) == 2 else results[0]
            if ok and x['path']:
                preview = x['path']
        # - Save to storage.
        doc = {}
        if thumbnail:
            blob = storage_client.blob(f'manga/{manga_id}/{self.path_leaf(thumbnail)}')
            blob.upload_from_filename(self.store._get_filesystem_path(thumbnail))
            doc['thumbnail_url'] = blob.media_link
        if preview:
            blob = storage_client.blob(f'manga/{manga_id}/{self.path_leaf(preview)}')
            blob.upload_from_filename(self.store._get_filesystem_path(preview))
            doc['preview_url'] = blob.media_link
        # - Save the download url to firestore.
        if doc:
            db_client.collection(self.root_collection).document(manga_id).set(doc, merge=True)
        return item

    def path_leaf(self, path):
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

class AhaMangaChapterDataPipeline:
    root_collection = 'aha_manga'
    chapters_collection = 'chapters'

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        manga_id = get_str(adapter['manga_id'])
        lang_ver = get_str(adapter['lang_version'])
        chapters = adapter['chapters']
        if type(chapters) is not list:
            raise DropItem('invalid [chapters] item')
        chapters_ref = db_client.collection(self.root_collection).document(manga_id).collection(self.chapters_collection)

        for chapter in chapters:
            chapter_id = chapter['chapter_id']
            chapter_url = chapter['chapter_url']
            chapter_doc = {}
            if lang_ver == 'en':
                chapter_doc['en_version'] = chapter_url
            elif lang_ver == 'ja':
                chapter_doc['ja_version'] = chapter_url
            elif lang_ver == 'vi':
                chapter_doc['vi_version'] = chapter_url
            else:
                logger.warn(f'invalid chapter version.')
                raise DropItem('the lang_version is invalid.')
            chapters_ref.document(chapter_id).set(chapter_doc, merge=True)

class AhaMangaChapterCrawlerStatusPipeline:
    root_collection = 'aha_crawler'

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        chapters = adapter['chapters']
        last_chapter = chapters[-1]['chapter_id']

        inst_id = get_str(adapter['inst_id'])
        cron_time = get_str(adapter['cron_time'])
        now = datetime.datetime.now()
        cron = croniter.croniter(cron_time, now)
        next_time = cron.get_next(datetime.datetime)

        db_client.collection(self.root_collection).document(inst_id).set({
            u'next_time': next_time,
            u'last_chapter': last_chapter
        }, merge=True)