from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pymysql
import random

# import lxml
# 定义 jiexi()函数，用于解析得到的 html
def jiexi(html, info, name):
	# print(html)
	soup = BeautifulSoup(html, "html.parser")
	text = soup.find_all("script", type="text/javascript")  # [2].string
	text = str(text).split('window.__SEARCH_RESULT__')[1]
	text = text.split("</script>, ")[0]
	# print('————————————————————————————————————————')
	# print(text)
	# 观察原始代码发现我们需要的数据在 engine_jds 后
	data = eval(text.split("=", 1)[1])["engine_jds"]
	for d in data:
		try:
			job_name = d["job_name"].replace("\\", "")  # 岗位名称
		except:
			job_name = " "
		try:
			company_name = d["company_name"].replace("\\", "")  # 公司名称
		except:
			company_name = " "
		try:
			providesalary_text = d["providesalary_text"].replace("\\", "")  # 薪资
		except:
			providesalary_text = " "
		try:
			workarea_text = d["workarea_text"].replace("\\", "")  # 工作地点
		except:
			workarea_text = " "
		try:
			updatedate = d["updatedate"].replace("\\", "")  # 更新时间
		except:
			updatedate = " "
		try:
			jobwelf = d["jobwelf"].replace("\\", "")  # 工作待遇
		except:
			jobwelf = " "
		try:
			companyind_text = d["companyind_text"].replace("\\", "")  # 公司类型
		except:
			companyind_text = " "
		try:
			companysize_text = d["companysize_text"].replace("\\", "")  # 公司规模
		except:
			companysize_text = " "
		try:
			at = d["attribute_text"]  # 工作要求
			s = ''
			for i in range(0, len(at)):
				s = s + at[i] + ','
			attribute_text = s[:-1]
		except:
			attribute_text = " "
		# 将每一条岗位数据爬取下的内容以及传入参数 name 作为一个列表，依此加入到info 列表中
		info.append([name, job_name, updatedate, company_name, companyind_text, companysize_text, workarea_text,
		             providesalary_text, attribute_text, jobwelf])


# 将数据存到 MySQL 中名为“51job”的数据库中
def save(data):
	db = pymysql.connect(  # 连接数据库
		host="127.0.0.1",  # MySQL 服务器名
		user="root",  # 用户名
		password="123456",  # 密码
		database="Python上机",  # 操作的数据库名称
		charset="utf8"
	)

	cursor = db.cursor()
	# 将数据保存到数据库表中对应的列
	for each_data in data:
		present_job = each_data[0]  # 当前爬取岗位
		job_name = each_data[1]  # 岗位
		updatedate = each_data[2]  # 更新时间
		company_name = each_data[3]  # 公司名称
		companyind_text = each_data[4]  # 公司类型
		companysize_text = each_data[5]  # 公司规模
		workarea_text = each_data[6]  # 工作地点
		providesalary_text = each_data[7]  # 薪资
		attribute_text = each_data[8]  # 工作要求
		jobwelf = each_data[9]  # 工作待遇
		# 创建 sql 语句
		sql = "insert into jobs(当前爬取岗位, 岗位, 更新时间,公司名称,公司类型,公司规模, \
		工作地点,薪资,工作要求,工作待遇) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		# 执行 sql 语句
		cursor.execute(sql, [present_job, job_name, updatedate, company_name, companyind_text, companysize_text,
		                     workarea_text, providesalary_text, attribute_text, jobwelf])
		db.commit()  # 提交数据库
	cursor.close()  # 关闭游标
	db.close()  # 关闭数据库


if __name__ == '__main__':  # 主函数
	# searchword = input('请输入你想查询的岗位：') # 自行输入 30 个岗位名称搜索
	# pages = int(input('请输入需要爬取的总页数：')) # 在观察后输入数据页面爬取数据
	searchword = '交互设计'  # 自行输入 30 个岗位名称搜索
	pages = 30  # 在观察后输入数据页面爬取数据
	mainurl = 'https://www.51job.com'  # 设置 51jobs 首页的url
	option = webdriver.ChromeOptions()
	option.add_experimental_option('excludeSwitches', ['enable-automation'])
	option.add_experimental_option('useAutomationExtension', False)
	browser = webdriver.Chrome(options=option)
	browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
	                        {"source":
		                    """
							Object.defineProperty(navigator, 'webdriver', {
							get: () => undefined
							})
							"""
	                         })
	browser.get(mainurl)  # 打开 51jobs 首页
	browser.implicitly_wait(random.randint(6, 12))
	browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[1]/div/div/p[1]/input').send_keys(
		searchword)  # 在搜索框输入要查询的岗位
	browser.implicitly_wait(random.randint(6, 12))
	button1 = browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[1]/div/button')  # 寻找搜索按钮
	button1.click()  # 点击搜索按钮
	time.sleep(random.randint(6, 12))
	windows = browser.window_handles
	browser.switch_to.window(windows[-1])
	info = []  # 空列表，传入 jiexi 函数用于存储每一条岗位的数据
	for i in range(1, pages + 1):
		# html = browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]').text
		# browser.refresh()
		html = browser.page_source  # 获取网页的 html
		browser.implicitly_wait(random.randint(6, 12))
		jiexi(html, info, searchword)
		if i <= 5:
			button2 = browser.find_element(By.XPATH,
			                               value='/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/ul/li[{}]/a'.format(i + 7))
		else:
			button2 = browser.find_element(By.XPATH,
			                               value='/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/ul/li[13]/a')  # 寻找下一页的按钮
		button2.click()  # 翻到下一页
		time.sleep(random.randint(6, 12))
		windows = browser.window_handles
		browser.switch_to.window(windows[-1])
		browser.get(browser.current_url)
		time.sleep(4)
	save(info)
	print('{}岗位的{}页数据已经爬取成功！请进入 Mysql 数据库检查！'.format(searchword, pages))
