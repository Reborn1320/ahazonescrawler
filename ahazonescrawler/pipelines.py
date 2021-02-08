# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import ntpath
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from ahazonescrawler.firebase.admin import db_client, storage_client


class AhazonescrawlerPipeline:
    def process_item(self, item, spider):
        return item

# This pipeline to use insert manga info into firestore
class AhaMangaInfoDataPipeline:
    root_collection = 'aha_manga'

    def open_spider(self, spider):
        logging.info('Start inserting manga info data')

    def close_spider(self, spider):
        logging.info('Stop inserting manga info data')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # save info to firestore.
        db_client.collection(self.root_collection)
            .document(adapter['manga_id'])
            .set({
            u'author': adapter['author_inf'],
            u'categories': adapter['categories_inf']
            u'summary': adapter['summary_inf']
        })
        # return item to the next pipeline.
        return item

#
class AhaMangaInfoThumbnailPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['thumbnail_url'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # - Save to storage.
        file_name = self.path_leaf(image_paths[1])
        blob = storage_client.blob(f'{item['manga_id']}/{file_name}')
        blob.upload_from_filename(image_paths[1])
        # - TODO: save the path to firestore
        return item

    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)