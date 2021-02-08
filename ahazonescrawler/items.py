# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class AhazonescrawlerItem:
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

@dataclass
class AhaMangaInfoItem:
    manga_id: str
    author_inf: str
    categories_inf: str
    summary_inf: str
    thumbnail_url: str
    preview_url: str