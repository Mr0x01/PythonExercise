from scrapy.cmdline import execute
name = "mm131spider"
cmd = "scrapy crawl {0}".format(name).split()
execute(cmd)
