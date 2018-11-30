import os, cv2
import numpy as np
from collections import Counter


class KnnUtil():
    """
    Knn工具类
    """
    __trainedDataList = np.array([])
    __k_count = np.array([])
    __K = 0

    def __init__(self, K):
        marked_imgs = os.listdir("train\\sliced")
        for marked_img in marked_imgs:
            img_object = cv2.imread("train\\sliced\\" + marked_img,
                                    cv2.IMREAD_UNCHANGED)
            plat = np.reshape(img_object,-1)
            value = int(marked_img.split("-")[0])
            plat = np.append(plat, value)
            self.__trainedDataList = np.append(self.__trainedDataList, [plat])
        self.__trainedDataList = np.reshape(self.__trainedDataList,(-1,181))
        self.__K = K

    def __calcEuclideanDistance(self, a, b):
        """
        计算欧式距离
        """
        if self.__trainedDataList == []:
            raise "未初始化"
        else:
            temp = 0
            for x in range(len(a)):
                temp += (a[x] - b[x]) * (a[x] - b[x])
            temp = np.sqrt(temp)
            return temp

    def calssify(self, img):
        """
        分类
        """
        distance = np.array([9 * 20 * 256 for x in range(self.__K)])
        values = np.array([-1 for i in range(self.__K)])
        for i in range(len(self.__trainedDataList)):
            d = self.__calcEuclideanDistance(np.reshape(img,-1),self.__trainedDataList[i])
            for k in range(self.__K):
                if distance.item(k) > d:
                    distance[k] = d
                    values[k] = self.__trainedDataList[i][-1]
                    break
        result = Counter(values).most_common(1)[0]
        return result
