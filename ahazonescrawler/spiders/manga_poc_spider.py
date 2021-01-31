import scrapy

class MangaPocSpider(scrapy.Spider):
    name = "mangaPoc"

    def start_requests(self):
        urls = [
            'http://truyentranhtuan.com/one-piece/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        manganame = response.url.split("/")[-2]
        filename = f'{manganame}.txt'

        # get description
        descriptionEle = response.css('div#manga-summary')
        description = descriptionEle.css('p::text').get()

        # get author
        authorEle = response.css('[itemprop=author]')
        author = authorEle.css('[itemprop=name]::text').get()
        if author is not None:
            author = author.strip()

        # get category
        rawCategories = response.css('a[itemprop=genre]::text').getall()       
        categories = []
        for category in rawCategories:
            categories.append(category.strip())
        
        # get thumbnail image
        thumbnailEle = response.css('div.manga-cover')
        thumbnailUrl = thumbnailEle.css('img').attrib['src']

        with open(filename, 'w') as f:
            f.write('author: ' + author)
            f.write('\n')
            f.write('categories: ' + ', '.join(categories))
            f.write('\n')
            f.write('thumbnailUrl: ' + thumbnailUrl)
            f.write('\n')
            f.write('description: ' + description)
        self.log(f'Saved file {filename}')