import cv2 as cv
import os
from img_util import ImgUtil


if os.path.exists("binary") == False:
    os.mkdir("binary")
if os.path.exists("sliced") == False:
    os.mkdir("sliced")
if os.path.exists("gray") == False:
    os.mkdir("gray")
binary = cv.imread("sliced\\1543481383.1247933-4.png")
ImgUtil.drawImgArray(binary)
# files = os.listdir("imgs")
# for file in files:
#     img = cv.imread("imgs\\" + file, cv.IMREAD_COLOR)
#     gray = ImgUtil.toGray(file, img)
#     binary = ImgUtil.toBinary(file, gray)
#     ImgUtil.sliceImg(file, binary)
