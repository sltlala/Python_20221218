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
	cursor.execute("select * from jobs")  # 从 jobs 表中查询所有内容并保存
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
		# 剩余岗位需 要两个关键词都存在岗位名称中，例如包含“数据”或“分析”在以“数据分析”
		# 为关键词搜索的岗位名称种，我们就认为匹配成功。
	cursor.close()  # 关闭游标
	return after_pipei  # 返回匹配后的列表