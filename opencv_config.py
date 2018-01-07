#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-01-06 13:23:44
# @Author  : Bob Liao (codechaser@163.com)
# @Link    : https://github.com/coderchaser


'''
	完全Opencv的半自动微信跳一跳，原理参照了@wangshub的开源项目wechat_jump_game,地址：
				https://github.com/wangshub/wechat_jump_game
				另外，机型参数也使用了wechat_jump_game的参数。
	感谢@wangshub的许可以及社区前辈们的贡献。
	使用方法：cmd 运行：python opencv_wechat_jump.py
'''

import os
import sys
import json
import re
import subprocess
import time
def get_screen_size():
	'''
	获取手机屏幕分辨率
	'''
	# process=subprocess.Popen("adb wm size",shell=True,stdout=subprocess.PIPE)
	stdout_result=os.popen("adb shell wm size").read()
	try:
		if not stdout_result :
			raise RuntimeError("请确保已经安装了ADB并配置好了环境变量，Android手机连接正常打开USB调试模式后重新运行程序")
	except RuntimeError as e:
		print(e)
		sys.exit()
	size=re.search(r"(d+) (d+)",stdout_result)
	if size :
		return "{height}x{width}".format(size.group(2),size.group(1))
	return "1920x1080"

def get_config():
	'''
	获取配置参数
	'''
	screen_size=get_screen_size()
	print("手机屏幕分辨率为：%s" %screen_size)
	config_path=sys.path[0]
	config_file_path="{config_path}/config/{screen_size}/config.json".format(
		config_path=config_path,
		screen_size=screen_size)
	if os.path.exists(config_file_path):
		print("从以下路径加载配置文件 \n {}".format(config_file_path))
		with open(config_file_path,"r") as f :
			#私以为在with语句里面返回不好，会不会造成文件没有成功关闭呢？
			json_data=json.load(f)
		return json_data
	else :
		fp="{config_path}/config/default.json"
		print("从默认路径加载配置文件 :{}".format(fp))
		with open(fp,"r") as f :
			json_data=json.load(f)
		return json_data


