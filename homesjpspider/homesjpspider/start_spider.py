import logging
from scrapy.cmdline import execute
name = "homesjpspider"
cmd = "scrapy crawl {0}".format(name).split()
try:
    execute(cmd)
except BaseException as identifier:
    logging.error(identifier.__dict__)
    raise identifier
