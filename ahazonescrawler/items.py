# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AhazonescrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AhaMangaInfoItem(Item):
    inst_id = Field()
    manga_id = Field()
    author_inf = Field()
    categories_inf = Field()
    summary_inf = Field()
    thumbnail_url = Field()
    preview_url = Field()

class AhaMangaChaptersItem(Item):
    inst_id = Field()
    manga_id = Field()
    lang_version = Field()
    cron_time = Field()
    chapters = Field()