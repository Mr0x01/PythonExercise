# 某人力资源系统验证码识别（基于KNN）
![示意图](https://raw.githubusercontent.com/Mr0x01/PythonExercise/master/captcha_recognition/3.png)
## 起因
本来想爬一份自己的工资表，但是在自动登陆的时候有验证码，之前偷懒用手动复制Session的方法绕过了，但心有不甘，所以就学习一下吧。
## 经过
### 分析
下载了十几个验证码样本后发现：
1. 没有字母，只有数字，且固定是4位
2. 没有翻转、倾斜、变形
3. 有干扰线，颜色与字符相同
4. 没有背景杂色和噪点
5. 字符只有上下浮动，左右位置固定
这就少了许多识别前的负担，尤其是字符左右位置固定，在切分的时候就很容易了。
### 处理
就用了常规步骤，灰度→计算阈值→二值化图片→切分图片→识别 <br /><br />
要说的是，阈值用了很笨的办法计算：把所有非白色的灰度相加÷总非白色像素数
### 训练
KNN其实没有要训练的，主要训练的是我的打字速度。第一批400个“邻居”是我自己手动打的码，还好只有0~9这十个数字。
## 结果
在加载400个样本，K设置为5，对训练集进行测试本身进行测试时，准确率达到了91%，这个准确率还算凑合吧。后将样本数量翻倍为800个，测试了10张全新图片后，只有1张识别错误（将9识别为了0）<br/>
![矩阵图1](https://raw.githubusercontent.com/Mr0x01/PythonExercise/master/captcha_recognition/1.png)
![矩阵图2](https://raw.githubusercontent.com/Mr0x01/PythonExercise/master/captcha_recognition/2.png)