# 引入 pymysql 包
import pymysql

# 连接 MySQL 数据库
db = pymysql.connect(
	host="127.0.0.1",
	user="root",
	password="123456",
	database="Python上机",
	charset="utf8"
)


def pipei():
	cursor = db.cursor()  # 获取操作游标
	cursor.execute("select * from jobs2")  # 从 jobs 表中查询所有内容并保存
	results = cursor.fetchall()  # 接受全部的返回结果
	after_pipei = []  # 建立一个空列表，用来存储匹配后数据
	for each_result in results:
		if each_result[-1] == '物流与供应链':
			if '物流' in each_result[0] or '供应链' in each_result[0]:
				after_pipei.append(each_result)
		elif each_result[-1] == '新媒体运营' or each_result[-1] == '电商运营':
			if '运营' in each_result[0]:
				after_pipei.append(each_result)

		# 由于在 以关键词“电商运营”或“新媒体运营”搜索的岗位信息中包含大量具体电商或新媒体平台名称的岗位名称，
		# 如“拼多多运营”“抖音运营”等，因此在这两类 岗位名称匹配时我们认为只要岗位名称中包含“运营”就算匹配成功。

		elif each_result[-1] == '客户关系管理':
			if '客户关系' in each_result[0]:
				after_pipei.append(each_result)
		elif each_result[-1] == '安卓开发':
			if '安卓' in each_result[0] or 'Android' in each_result[0]:
				after_pipei.append(each_result)

		# 由于在很多公司的招聘岗位中“安卓”会以“Android”英文形式出现，因此，在以“安卓开发”为关键词进行搜索时，
		# 我们认为只要包含“安卓”或“Android”开发 就算匹配成功。

		elif each_result[-1][:-2] in each_result[0] and each_result[-1][-2:] in each_result[0]:
			after_pipei.append(each_result)

		# 剩余岗位需要两个关键词都存在岗位名称中，例如包含“数据”或“分析”在以“数据分析”
		# 为关键词搜索的岗位名称种，我们就认为匹配成功。

	cursor.close()  # 关闭游标
	return after_pipei  # 返回匹配后的列表


def split_city(data):
	after_split_city = []  # 建立一个空列表，用来存储匹配后数据
	for each_date in data:
		each_date_list = list(each_date)
		each_date_list[5] = each_date_list[5].split('-')[0]  # 将数据表中工作地点列以'-'进行切割，选取第一个元素替换
		# print(each_date_list)
		after_split_city.append(each_date_list)
	return after_split_city  # 返回筛除后的数据


def salary_1(data):  # 清除工作薪资内容的“·xx 薪”
	after_salary_1 = []
	for each_data in data:
		if '千' in each_data[6] and '万' in each_data[6]:
			if '千' in each_data[6]:
				each_data[6] = str((float(each_data[6].split('千')[0]) / 10)) + each_data[6].split('千')[1]
			if '及以下' in each_data[6]:
				each_data[6] ='30.0千/月'
		if '薪' in each_data[6]:
			each_data[6] = each_data[6].split('·')[0]
		after_salary_1.append(each_data)
	return after_salary_1


def salary(data):
	after_salary = []  # 建立一个空列表，用来存储匹配后数据
	for each_data in data:
		if each_data[6] != '':  # 筛除缺失值，以小时 计费，给出的薪资表达为在“……以下”及“……以上”等难以计算数据的工作岗位#统一量纲（单位:千/月）
			if each_data[6][-1] == '年':
				try:
					each_data[6] = str((float(each_data[6].split('万')[0].split('-')[0]) + float(
						each_data[6].split('万')[0].split('-')[1])) * 5 / 12) + '千/月'
				except:
					each_data[6] = each_data[6]
			elif each_data[6][-1] == '天':
				try:
					each_data[6] = str(float(each_data[6].split('元')[0]) * 30 / 1000) + '千/月'
				except:
					each_data[6] = each_data[6]
			elif each_data[6][-1] == '万':
				try:
					each_data[6] = str((float(each_data[6].split('万')[0].split('-')[0]) + float(
						each_data[6].split('万')[0].split('-')[1])) * 5) + '千/月'
				except:
					each_data[6] = each_data[6]
			else:
				try:
					each_data[6] = str((float(each_data[6].split('千')[0].split('-')[0]) + float(
						each_data[6].split('千')[0].split('-')[1])) / 2) + '千/月'
				except:
					each_data[6] = each_data[6]
			after_salary.append(each_data)
		# print(after_salary)
	return after_salary  # 返回平均工资后的数据


def job_attribute_text(data):
	for each_data in data:
		# 因为爬取到的工作要求内容中的情况多样，如“东莞-松山湖区,5-7 年经验,大专”等，需要做出多种判断。
		# 最后只保留“经验，学历”形式的数据内容，若经验或学历为空，保留形式为“，学历”或“经验，”方便后续选用。
		# 以“，”切割后的列表长度为 3，若包含了“经验”元素，则保留“经验，”形式内容
		if len(each_data[7].split(',')) == 3:
			each_data[7] = each_data[7].split(',')[1] + ',' + each_data[7].split(',')[2]
		elif len(each_data[7].split(',')) == 2:
			each_data[7] = each_data[7].split(',')[1] + ','
		else:
			each_data[7] = ''
	# 返回筛除后的数据 #将清洗后的数据保存到数据库中 after_clean表中，代码和保存爬取数据时类似
	return data


def save(data):
	cursor = db.cursor()
	for each_data in data:
		job_name = each_data[0]
		updatedate = each_data[1]
		company_name = each_data[2]
		companyind_text = each_data[3]
		companysize_text = each_data[4]
		workarea_text = each_data[5]
		providesalary_text = each_data[6]
		attribute_text = each_data[7]
		jobwelf = each_data[8]
		present_job = each_data[9]
		sql = "insert into after_clean(当前爬取岗位,岗位,更新时间,公司名称,公司类型,公司规模,\
		工作地点,薪资,工作要求,工资待遇)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql, [present_job, job_name, updatedate, company_name, companyind_text, companysize_text,
		                     workarea_text, providesalary_text, attribute_text, jobwelf])
		db.commit()
	cursor.close()
	db.close()


# 定义主函数，用以执行以上四步数据清洗过程
if __name__ == '__main__':
	data = pipei()
	# print(data[:10])
	data1 = split_city(data)
	# print(data1[:10])
	data2 = salary_1(data1)
	# print(data2[:20])
	data3 = salary(data2)
	# print(data2[:10])
	data4 = job_attribute_text(data3)

	data5 = list(set(tuple(i) for i in data4))  # 转化为元组做主键
	# NewList = [list(t) for t in set(tuple(i) for i in List)]
	# data5.sort(key=data4.index)
	# print(data5[:10], '\n', type(data5))
	save(data5)
