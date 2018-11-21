import hashlib

class Hash_Util:

    @staticmethod
    def sha1(str):
        myhash = hashlib.sha1(str.encode('utf-8'))
        return myhash.hexdigest()