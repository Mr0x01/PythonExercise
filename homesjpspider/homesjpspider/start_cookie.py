import logging
from scrapy.cmdline import execute
name = "homesjpcookie"
cmd = "scrapy crawl {0}".format(name).split()
try:
    execute(cmd)
except BaseException as identifier:
    logging.error(identifier.__dict__)
    raise identifier
