import logging
from scrapy.cmdline import execute
name1 = "homesjpcookie"
name2 = "homesjpspider"
cmd = "scrapy crawl {0}".format(name2).split()
try:
    execute(cmd)
except BaseException as identifier:
    logging.error(identifier.__dict__)
    raise identifier
