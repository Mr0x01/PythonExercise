from img_util import ImgUtil
from knn_util import KnnUtil
import cv2 as cv
import os,time
if os.path.exists("imgs") == False:
    os.mkdir("imgs")
if os.path.exists("binary") == False:
    os.mkdir("binary")
if os.path.exists("sliced") == False:
    os.mkdir("sliced")
if os.path.exists("gray") == False:
    os.mkdir("gray")
if os.path.exists("result") == False:
    os.mkdir("result")

# ImgUtil.mark_img()
knn = KnnUtil(5)
ImgUtil.collect_img(10)
files = os.listdir("imgs")
for file in files:
    img = cv.imread("imgs\\" + file, cv.IMREAD_COLOR)
    gray = ImgUtil.toGray(file, img)
    binary = ImgUtil.toBinary(file, gray)
    ImgUtil.drawImgArray(binary)
    piece = ImgUtil.sliceImg(file, binary)
    result = ""
    for item in piece:
        val = str(knn.calssify(item)[0])
        result += val
        # cv.imwrite("result\\"+val+"-"+str(time.time())+".png",item)
    cv.imwrite("result\\"+result+".png",img)
    
    print(result)
    
    