import logging
from scrapy.cmdline import execute
name = "homesjpspider"
cmd = "scrapy crawl {0}".format(name).split()
try:
    execute(cmd)
except Exception as identifier:
    logging.error(identifier.__dict__)
