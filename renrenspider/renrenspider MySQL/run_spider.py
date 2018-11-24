from scrapy import cmdline
name = "renrenspider"
cmd = "scrapy crawl {0}".format(name).split()
cmdline.execute(cmd)