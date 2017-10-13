#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, time, csv
from selenium import webdriver

# 加载浏览器驱动
def load_driver(driver_path = '/usr/local/bin/chromedriver'):
	reload(sys)
	sys.setdefaultencoding('utf-8')

	# 高度多一点，省得翻页
	WIDTH = 640
	HEIGHT = 10000
	PIXEL_RATIO = 3.0
	UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'

	options = webdriver.ChromeOptions()
	options.add_experimental_option('mobileEmulation', {
		'deviceMetrics': {
			'width': WIDTH,
			'height': HEIGHT,
			'pixelRatio': PIXEL_RATIO
		},
		'userAgent': UA
	})

	return webdriver.Chrome(driver_path, chrome_options = options)

def execute(args = []):
	try:
		print('加载浏览器驱动...')
		driver = load_driver(args.pop(0))
		print(driver)

		# TODO这里可以改成从文件里读链接
		# driver.get就是模拟访问网页的动作
		print('访问页面中...')
		driver.get('http://m.1688.com/winport/company/b2b-2924437638805ea.html?spm=a26g8.9831716.0.0')
		time.sleep(5)

		# 基本信息
		list_title = driver.find_elements_by_css_selector("div[class=archive-baseInfo-companyInfo]>ul[class=info-item]>li>div[class=info-container]>em")
		list_item = driver.find_elements_by_css_selector("div[class=archive-baseInfo-companyInfo]>ul[class=info-item]>li>div[class=info-container]>span")

		row1 = []
		row2 = []

		for i in xrange(len(list_title)):
			title = list_title[i].text.strip(' :')
			row1.append(title.encode('gbk'))
			print('添加列--->' + title)
			row2.append('	' + list_item[i].text.encode('gbk'))

		# 联系人信息
		list_title = driver.find_elements_by_css_selector("div[class=archive-baseInfo-container]>div[id=scroller]>div[class=archive-baseInfo-contactInfo] ul[class=info-item] li div[class=info-container] em")
		list_item = driver.find_elements_by_css_selector("div[class=archive-baseInfo-container]>div[id=scroller]>div[class=archive-baseInfo-contactInfo] ul[class=info-item] li div[class=info-container] span")

		for i in xrange(len(list_title)):
			title = list_title[i].text.strip(' :')
			row1.append(title.encode('gbk'))
			print('添加列--->' + title)
			row2.append('	' + list_item[i].text.encode('gbk'))

		# 第二页需要点一下tab才能显示元素
		page_tabs = driver.find_elements_by_css_selector('ul.tab-navs>li>div.archive-menu-tab')

		if len(page_tabs) > 1:
			page_tabs[1].click()

		# 标签上的文字
		row1.append('企业能力标签'.encode('gbk'))

		tags = driver.find_elements_by_css_selector('div[class=info-tag-list]>a[class=info-tag]')

		temp_str = ''
		for i in xrange(len(tags)):
			temp_str += tags[i].text + ', '

		row2.append(temp_str.strip(', ').encode('gbk'))

		row1.append('认证信息-->'.encode('gbk'))
		row2.append('----->---->'.encode('gbk'))

		list_title = driver.find_elements_by_css_selector('div[class=archive-authinfo-mod]>ul[class=info-item]>li>div[class=info-container]>em')
		list_item = driver.find_elements_by_css_selector('div[class=archive-authinfo-mod]>ul[class=info-item]>li>div[class=info-container]>span')

		for i in xrange(len(list_title)):
			title = list_title[i].text.strip(' :')
			row1.append(title.encode('gbk'))
			print('添加列--->' + title)
			row2.append('	' + list_item[i].text.encode('gbk'))

		# 最后一步
		# 创建csv
		csvfile = file(args.pop(0), 'web')
		writer = csv.writer(csvfile)

		# 点击一下联系按钮，显示出包含电话的div
		driver.find_element_by_class_name('archive-contact-phone').click()
		phone = driver.find_element_by_css_selector('div.archive-sheet-item.phone').text
		# 给第二列插入电话
		row1.insert(1, u'联系电话'.encode('gbk'))
		row2.insert(1, '	' + phone)

		writer.writerow(row1)
		writer.writerow(row2)

		# 关闭csv
		csvfile.close()
		# 关闭模拟浏览器
		driver.close()

	except Exception as e:
		print('\033[0;31mError!!!')
		print(e)
		print('\033[0m')
	finally:
		print('\033[0;32mDone.\033[0m')
		sys.exit(0)

if __name__ == '__main__':
	args = sys.argv

	if  len(args) < 3:
		print('缺少driver路径参数、目标文件参数')
	else:
		# 去除脚本文件名
		args.pop(0)
		execute(args)
