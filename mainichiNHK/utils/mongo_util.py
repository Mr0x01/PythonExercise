import pymongo


class MongoUtil:
    def __init__(self):
        #self.CS = "mongodb://root:1q2w#E$R@10.20.10.98/mainichiNHK?authSource=admin"
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017, connect=False)
