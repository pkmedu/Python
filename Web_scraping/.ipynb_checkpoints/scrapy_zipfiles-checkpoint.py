# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.pipelines.files import FilesPipeline


class ZipfilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        filename = request.url.split("/")[-1]
        return f"zipfiles/{filename}"


class MepsSpider(CrawlSpider):
    name = "meps_spider"
    allowed_domains = ["meps.ahrq.gov"]
    start_urls = ["https://meps.ahrq.gov/data_files/pufs/"]
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0",
        "ITEM_PIPELINES": {"apc.spiders.meps_spider.ZipfilePipeline": 1},
        "FILES_STORE": "./",
    }

    rules = (
        Rule(
            LinkExtractor(
                allow=r"https://meps.ahrq.gov/data_files/pufs/(.*)",
                restrict_css=r"table td",
                deny_extensions=("zip", "exe", "shtml"),
            ),
            callback="parse_page",
            follow=False,
        ),
    )

    def parse_page(self, response):
        zipfile_urls = []
        link_extractor = LinkExtractor(
            allow=r"(.*).zip",
            deny_extensions=(),
        )
        for zipfile in link_extractor.extract_links(response):
            zipfile_urls.append(zipfile.url)
            # Comment out the following line to download the zipfiles
            yield {"url": zipfile.url}
        # Uncomment the following lines to download the zipfiles.
        # return {"file_urls": zipfile_urls}