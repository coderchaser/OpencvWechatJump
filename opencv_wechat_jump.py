#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-01-04 23:42:48
# @Author  : Bob Liao (codechaser@163.com)
# @Link    : https://github.com/coderchaser


'''
	完全Opencv的半自动微信跳一跳，原理参照了@wangshub的开源项目wechat_jump_game,地址：
				https://github.com/wangshub/wechat_jump_game
				另外，机型参数也使用了wechat_jump_game的参数。
	感谢@wangshub的许可以及社区前辈们的贡献。
	使用方法：cmd/shell 运行：python opencv_wechat_jump.py
'''

import numpy as np
import cv2
import time
import os
import subprocess
import math
import random
import logging
import opencv_config



#log文件
LOG_FILE="./wechatJump.log"
if os.path.isfile(LOG_FILE) :
	os.remove(LOG_FILE)
logging.basicConfig(filename=LOG_FILE,level=logging.INFO)
#缩放系数，视机型决定，因为我的是1920x1080,所以我没用缩放，如果你是别的机型，按比例缩#shrink=0.25
#棋子模板
template=cv2.imread('./config/character.png')
# template=cv2.resize(template,None,fx=shrink,fy=shrink,interpolation=cv2.INTER_AREA)
#54 22 3 shape
template_size=template.shape[:2]
#获取按压时间与距离间的系数
press_time_rate=opencv_config.get_config()["press_coefficient"]
print("设定按压时间与距离系数为：%s" %press_time_rate)
logging.info(u"press_time_rate :{rate},{time}".format(rate=press_time_rate,time=time.time()))
#棋子位置
src_x=0;src_y=0




def search(img) :
    '''
    用来比对模板，找出棋子位置
    @param img:需要匹配的图片
    return 图片img及匹配位置
    '''
    #采用cv2.TM_SQDIFF方法匹配
    result_image=cv2.matchTemplate(img,template,cv2.TM_SQDIFF)
    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(result_image)
    cv2.rectangle(img,(min_loc[0],min_loc[1]),(min_loc[0]+template_size[1],min_loc[1]+template_size[0]),(0,0,255),4)
    #以底边中间位置为棋子横坐标，以最小匹配坐标加上模板高度为棋子纵坐标，减去20px可有效改善精度
    left_up_corner_x=min_loc[0]+template_size[1]/2
    left_up_corner_y=min_loc[1]+template_size[0]-20
    return img,left_up_corner_x,left_up_corner_y


def pull_screenshot():
	'''
	获取手机截图
	'''
	process=subprocess.Popen("adb shell screencap -p",stdout=subprocess.PIPE)
	screenshot=process.stdout.read()
	#我的Android手机支持PIPE方式，如果你的不支持，可以参照wangshub的代码修改
	binary_screenshot=screenshot.replace(b'\r\n',b'\n')
	with open("screen_shot.png","wb") as f :
		f.write(binary_screenshot)

def jump(distance) :
	'''
	棋子起跳
	@para distance:棋子与鼠标示意点距离
	return None
	'''
	press_time=distance*press_time_rate
	press_time=int(press_time)
	#随机按压位置
	input_x=random.randint(310,330)
	input_y=random.randint(400,420)
	cmd="adb shell input swipe {x} {y} {x} {y} {time}".format(x=input_x,y=input_y,time=press_time)
	print(cmd)
	logging.info(cmd)
	print("Press time: {time}".format(time=press_time))
	os.system(cmd)


def get_mouse_loc(event,x,y,flags,param) :
	'''
	通过鼠标来选取目标点
	'''
	global distance
	if event==cv2.EVENT_LBUTTONDOWN :
		distance=(x-src_x)**2+(y-src_y)**2
		distance=math.sqrt(distance)
		print("distance is : %f " % (distance))
		logging.info("distance is : %f " % (distance))
		jump(distance)
		#等待2S，棋子跳完
		time.sleep(2)
		#更新截图
		pull_screenshot()
	else :
		pass
def main():
	global src_x,src_y
	pull_screenshot()
	cv2.namedWindow(u"image",0)
	cv2.setMouseCallback(u"image",get_mouse_loc)
	img=cv2.imread("screen_shot.png")
	while 1:
		img,src_x,src_y=search(img)
		# cv2.imwrite("save.png",img)
		cv2.imshow(u"image",img)
		k=cv2.waitKey(20) & 0XFF
		#32位机器改为：
		#k=cv2.waitKey(20)
		img=cv2.imread("screen_shot.png")
		if k== 27 :
			break
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()





