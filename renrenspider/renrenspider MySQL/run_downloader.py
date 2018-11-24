from scrapy import cmdline
name = "renrendownloader"
cmd = "scrapy crawl {0}".format(name).split()
cmdline.execute(cmd)