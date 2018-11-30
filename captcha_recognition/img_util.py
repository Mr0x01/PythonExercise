import os
import time
import requests
import cv2 as cv


class ImgUtil:
    """
    图片处理工具类
    """

    @classmethod
    def mark_img(self):
        """
        对本sliced目录下已经切分完毕的字符图片进行标注
        标注会被记录在文件名上，格式为：时间戳-对应值
        """
        cv.startWindowThread()
        cv.namedWindow("preview")
        path = "result\\"
        for img in os.listdir(path):
            item = cv.imread(path + img)
            item_b = cv.resize(item, (18, 40), fx=3, fy=3)
            cv.imshow("preview", item_b)
            cv.waitKey(1)
            new = input("{0}:".format(img))
            if new !="" and new!=None:   
                os.rename(path + img, path + str(new) +"-" +  str(time.time()) + ".png")

    @classmethod
    def collect_img(self, amount=100):
        """
        采集验证码图片
        @para amount 可以指定采集的数量，默认为100
        """
        for i in range(amount):
            result = requests.request(
                "GET", "http://xxx.xxx.xxx/PlatinumHRM-ESS/WebPages/Common/Captcha.aspx")
            with open("imgs\\" + str(i) + ".png", 'wb') as file:
                file.write(result.content)

    @classmethod
    def toGray(self, name, img):
        """
        将图片转换为灰度化图片
        @para name 灰度后的文件名
        @para img  未灰度化的图片
        """
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        cv.imwrite("gray\\" + name, gray)
        return gray

    @classmethod
    def toBinary(self, name, img):
        """
        将图片二值化
        遍历所有像素点，计算出除了白色以外的灰度总值，除以白色像素以外的像素数得出灰度均值，
        此均值作为阈值，大于阈值的，设置为白色255，小于阈值的，设置为黑色0
        @para name 灰度后的文件名
        @para img  未灰度化的图片
        """
        height = img.shape[1]
        width = img.shape[0]
        sum_val = 0
        sum_pixel = 0
        for row in range(height):
            for col in range(width):
                val = img.item(col,row)
                if val != 255:
                    sum_val += val
                    sum_pixel += 1
        th = sum_val / sum_pixel
        for row in range(height):
            for col in range(width):
                val = img.item(col,row)
                if val < th:
                    img[col][row] = 0
                else:
                    img[col][row] = 255

        cv.imwrite("binary\\" + name, img)
        return img

    @classmethod
    def sliceImg(self, name, img):
        """
        切分图片
        由于样本图片的字符横轴定位几乎相同，所以采用了固定的切分方法
        @para name 切分后的文件名
        @para img  图片
        """
        #img[y: y + h, x: x + w]
        piece = []
        piece.append(img[0:20, 3:12])
        piece.append(img[0:20, 13:22])
        piece.append(img[0:20, 23:32])
        piece.append(img[0:20, 33:42])
        for i in range(4):
            cv.imwrite("sliced\\" + name + "-" + str(i) + ".png",
                       piece[i])
        return piece

    @classmethod
    def drawImgArray(self, img):
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                val = img.item(row, col)
                if val == 0:
                    val = "0"
                else:
                    val = " "
                print(val, end="")
            print("\r")
