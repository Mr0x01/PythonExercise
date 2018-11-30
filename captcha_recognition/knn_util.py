import os,cv2
import numpy as np

class KnnUtil():
    """
    Knn工具类
    """
    trainedDataList = []

    def __init__(self):
        marked_imgs = os.listdir("sliced")
        for marked_img in marked_imgs:
            img_object = cv2.imread("sliced\\"+marked_img,cv2.IMREAD_UNCHANGED)
            plat = np.reshape(img_object,1)
            

            