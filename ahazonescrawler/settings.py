# Scrapy settings for ahazonescrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ahazonescrawler'

SPIDER_MODULES = ['ahazonescrawler.spiders']
NEWSPIDER_MODULE = 'ahazonescrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ahazonescrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ahazonescrawler.middlewares.AhazonescrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ahazonescrawler.middlewares.AhazonescrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'ahazonescrawler.pipelines.AhazonescrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Firebase settings
# The service account credentials
FIREBASE_ADMIN_CREDENTIALS = {
    'type': 'service_account',
    'project_id': 'buzznews-8df38',
    'private_key_id': 'e344bd70c59393a73358aedeb8760a6cd0dbd7fd',
    'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0Eu0plJ7Qh7xe\nO4WNe+IIx3vleCFlEG1I8x8nTLgZYGHwSOKPqCFWDa15yZurSt+hAoMBPz4FxouP\ntOJqxnTWTAI9V5tlasdu+1EY70jiOXkW8enuC74O4ZEkkqMatcM5dNj+30AuxqeC\nivEWPZZUet2GmHC3iNYWh8Lex8Aov9sSPU0OnYHjLqQQUtJLGULEN9tspbfy23+3\n9+XfqMgjEPEyqwYoTD3xxc5BpsZJ2hrBt8t5vC3XAVxXV+cbvkxQUUYkq+XrKS9e\ngfpByP+V9tgwZGi4SWdSi49oR9Be10RVxHg/9Q5K6JOjH5Bsr8QySQGtb4X1/7b0\no8inDXihAgMBAAECggEAFB9fUDuy6ZOZeaBGItLapeeA0Vo0xSHqTHIao54fnnpW\nR28lni8IFqEtpwPf+OrDha8Nq6iBCk0vEE6C1LK7oKzavTcafuFJSv4biGFI8DrC\n7Mz4uqimQuxy9zbJsjTojXWgwA57kh6R3nUfTsBwGZ2nPqCvS9snLVpbbOC+eO8T\naSj1SMqDlixWb4puwCUCF4yAQpwQmATDiJ9Gl4rMxl/mNpsxofUu1sU6OjeL/J6k\nqp0gJakneBQTrjvjdY2KcrdqrOst8zJY2IMtaDC73Y7qggZbCmdmupPmVJitcMYE\nIEYcQJCIq55r0cBL9zHwIyQrov+AJnQGoZpaG67koQKBgQDpa8Tmwch1KubAiXm5\nF1a/pCmQ7BEaBdPjNqqrEl4nMP3u/bXo1YgY8chJGCphR6OFZR8QASwdSSKNp+9A\n5Ql2L1rG3VlZ19SafxeyPnl60kh2vM5p/Tu2copJCwiZ0M027L+7YEyGMa8u0WC0\nVEayfmLL/8FyG8Z66R8WIU7x+QKBgQDFfh5EgahhV3kRaSPb6/ODH4uzxK5Na12V\nbjR0tnyNXTnFjt4R+YwrbvkiHcQd+OkO/92fE6Jk/+md/4aDLCHYuVc05ee+aprk\n21wFp1YohdoJ0ag9YVLURMdNuP0TO8oWI5rs2DheAZc8OrtSVY1BIpyMOTgqeHaL\nWwa55Zxl6QKBgBJCuxGuYUdBRvITDzG6sK+nYRUUUrYtdIkW8r0VX8ZDH+p9cKi5\nY79H0vpc6JvZpeI+qfJvlQrpeMmKNL5n7JiRVdGu6VmM9/XqMWlhV9GS99ZKKP/D\nrtM0HLtgIJkf6537YXiALRxmcKUB/kW9Phaiqon5BSIvKBTffe4WRv3JAoGBAKTh\njW2OfkB+oiJKEFkcndpcLOtyCj+yopgOQRcr/8KaEZCBnZ+OI1tjs/WqukB3vkP6\nlFGqN8tw6N8zJV9AKiXhXxBX3WnZYOYuyZ4ivcjpL0dBVd+g8GEt5uNZzVgQc8CW\nC1MvlafOVjA/rIKp0FuQBPkBEIZMulPQNEZhj3h5AoGAIKGOTDZnkCZK9UZ0/KVS\n96B+gVYTaMPklgTeJi8+Eei3Wr6Wz9OZtHItAay3ikP+JIivvtwhaiufAh0rMbqX\n5AJSznPjNoeOBYgPB0Aj3Q351JIkg2ViAfXK3h75ZOD9rdP49rLwTU9scKGAfxsL\nRWN1e2VziahgxLTbX+J4UXM=\n-----END PRIVATE KEY-----\n',
    'client_email': 'firebase-adminsdk-xhcdl@buzznews-8df38.iam.gserviceaccount.com',
    'client_id': '110957821496134136355',
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xhcdl%40buzznews-8df38.iam.gserviceaccount.com'
}

FIREBASE_ADMIN_OPTIONS = {
    'storageBucket': 'buzznews-8df38.appspot.com'
}