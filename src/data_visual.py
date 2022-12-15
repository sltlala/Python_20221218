# 引入画图将使用到的库
import pymysql
import matplotlib.pyplot as plt
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
import numpy as np
import pandas as pd
from pyecharts.charts import Sankey
import jieba
from imageio import imread
from wordcloud import WordCloud

# 连接数据库
db = pymysql.connect(
	host="127.0.0.1",
	user="root",
	password="123456",
	database="python上机",
	charset="utf8")


# 描绘九小类岗位的市场需求的数量特征
def gangweishuliang_hist():  # 主函数调用的 gangweishuliang_hist()函数
	cursor = db.cursor()
	cursor.execute("select `当前爬取岗位` from after_clean")
	# 选出 30 个岗位关键词所在的列数据
	results = cursor.fetchall()
	jobs = ['产品经理', '产品助理', '交互设计', '前端开发', '软件设计', 'IOS开发', '业务分析', '安卓开发', 'PHP 开发', '业务咨询', '需求分析', '流程设计', '售后经理',
	        '售前经理', '技术支持', 'ERP 实施', '实施工程师', 'IT 项目经理', 'IT 项目助理', '信息咨询', '数据挖掘', '数据运营', '数据分析', '网络营销', '物流与供应链',
	        '渠道管理', '电商运营', '客户关系管理', '新媒体运营', '产品运营']
	count = []  # 创建一个空列表，用于存储每种岗位的数量值
	for i in range(len(jobs)):
		count.append(0)  # 先在空列表中创建 30 个 0 元素
	for each_result in results:
		for i in range(0, 30):
			if each_result[0] == jobs[i]:
				count[i] += 1
				continue  # 计算每种岗位的数量
	jobs_classification = ['技术管理类', 'IT 运维类', '技术开发类', '业务咨询类', '技术支持类', '数据运营类', '市场职能类', '产品运营类',
	                       '数据管理类']  # 将 30 种岗位划分为九小类
	counts = []  # 创建一个空列表，用于存储每小类岗位的数量值
	for i in range(len(jobs_classification)):
		counts.append(0)  # 先在空列表中创建 9 个 0 元素
	# 根据大纲中给出的分类表，依据 30 种岗位数量值，分别计算出九小类岗位的数量值
	counts[0] = count[0] + count[1] + count[2]
	counts[1] = count[17] + count[18]
	counts[2] = count[3] + count[4] + count[5] + count[6] + count[7] + count[8]
	counts[3] = count[9] + count[10] + count[11]
	counts[4] = count[12] + count[13] + count[14] + count[15] + count[16]
	counts[5] = count[21] + count[22]
	counts[6] = count[23] + count[24] + count[25]
	counts[7] = count[26] + count[27] + count[28] + count[29]
	counts[8] = count[19] + count[20]
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
	# 画柱状图
	fig, ax = plt.subplots(figsize=(10, 7))  # 定义图片的大小
	ax.bar(x=jobs_classification, height=counts,
	       color='r')  # x是所有柱子的下标的列表 jobs_classification，height 包含所有柱子的高度值的列表counts，width 每个柱子的宽度，本代码使用默认值。
	# align 柱子对齐方式，有两个可选值：center 和 edge，本代码使用默认值“center”。color 为每根柱子呈现的颜色。
	ax.set_title("岗位数量柱状图", fontsize=15)  # 为柱状图命名并设置字体大小
	for x, y in enumerate(counts):
		plt.text(x, y + 5, '%s' % y, ha='center')  # 为每根柱子加上数值
	plt.show()  # 展示图片
	cursor.close()  # 关闭操作游标


# 描绘所有岗位学历要求饼图
def xueli_pie():  # 主函数调用的 xueli_pie()函数
	cursor = db.cursor()
	cursor.execute("select `工作要求` from after_clean")  # 选出工作要求的列数据
	results = cursor.fetchall()
	xueli = []  # 创建一个空列表，用来装工作要求种的“学历“数据
	for each_result in results:
		if each_result[0] != '' and each_result[0].split(',')[1] != '':
			xueli.append(each_result[0].split(',')[1])
	after_quchong_xueli = list(set(xueli))  # 对学历去重复值，由于元组不能更改，转换为列表类型，便于后续操作
	after_quchong_xueli = ['在校生/应届生' if each == '在校生\\/应届生' else each for each in after_quchong_xueli]
	counts = []  # 创建一个空列表，用于装所有岗位信息中每一种学历的数量值
	for i in range(len(after_quchong_xueli)):
		counts.append(0)
	for each in xueli:
		for i in range(len(after_quchong_xueli)):
			if each == after_quchong_xueli[i]:
				counts[i] += 1  # 计算每种学历的数量值

	# 在画图前，先设置参数 explode，计算每个城市数据分析岗位占比，让占比小于 5%的城市在饼图中突出一部分
	a = []
	for i in range(0, len(after_quchong_xueli)):
		a.append(0)
	for i in range(0, len(after_quchong_xueli)):
		total = sum(counts[:len(after_quchong_xueli)])
		if (counts[i] / total) < 0.05:
			a[i] = 0.2  # 让占比小于 5%的城市突出
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
	plt.pie(x=counts, explode=a, labels=after_quchong_xueli,
	        autopct='%1.2f%%')  # x 为基本数据，labels 为给各个部分添加标签的列表，autopct 显示各部分比例，本例中调用%1.2f%%。
	plt.title('学历要求饼状图')  # 为饼图添加标题
	plt.show()  # 展示图片
	cursor.close()  # 关闭操作游标


# 描绘所有岗位公司规模的数量特征
def company_size():  # 主函数调用的 company_size()函数
	cursor = db.cursor()
	cursor.execute("SELECT `公司规模` FROM `after_clean`")  # 选出公司规模列
	results = cursor.fetchall()
	# 筛出非空数据，装进 size 列表中
	size = []
	for each_result in results:
		if each_result[0] != '' and each_result[0].split(',')[0] != '':
			size.append(each_result[0].split(',')[0])
	# 将公司规模类型去重复值，得到例如['少于 50 人', '1000-5000 人', '5000-10000 人', '50-150 人',
	# '150-500 人', '10000 人以上', '500-1000 人']的after_quchong 列表
	after_quchong = list(set(size))
	# 计算公司规模的类型数量 type_size
	type_size = len(after_quchong)
	# 计算每种公司规模的岗位数
	# 创建一个起始值为 0，有 type_size 各元素的 count_each_size 列表
	count_each_size = []
	for i in range(type_size):
		count_each_size.append(0)
	# 计算不同规模公司的岗位数量
	for each_size in size:
		for each in range(0, type_size):
			if each_size == after_quchong[each]:
				count_each_size[each] = count_each_size[each] + 1
		# 创建一个公司规模类型和数量一一对应的字典
	dic = {}
	for i in range(0, type_size):
		dic[count_each_size[i]] = after_quchong[i]
	# 本例希望画出经过排序后的图形，由于 sort 排序会直接改变列表原来的元素，因此本例先新建一个与 count_each_size 相同的 order 列表，再进行排序
	order = count_each_size
	order.sort()
	scale = []
	for i in range(0, type_size):
		scale.append(dic.get(count_each_size[i]))  # 通过字典，用新建的order 列表找到对应的公司规模类型，生成新的 scale 列表，此时两个列表中的元素是一一对应关系
	# 画图
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
	plt.barh(scale, count_each_size)  # 横放条形图函数 barh
	plt.xlabel('数量')  # x 轴名称
	plt.ylabel('规模')  # y 轴名称
	plt.title('公司规模')  # 图形名称
	for y, x in enumerate(count_each_size):
		plt.text(x + 0.1, y, "%s" % round(x, 1), va='center')  # 为每个柱子加上对应的数值，其中 round(x,1)是将 x 值四舍五入到一个小数位
	plt.show()  # 展示图形
	cursor.close()  # 关闭操作游标


# 所有岗位在各个城市的数量分布热力图
def gangweishuliang_heatmap():  # 主函数调用的 gangweishuliang_heatmap()函数
	cursor = db.cursor()
	cursor.execute("SELECT `工作地点` FROM `after_clean` ")
	all = cursor.fetchall()
	cities = []  # 创建一个空列表，用来装各个城市名称
	for each in all:
		if len(each[0]) == 2:
			cities.append(each[0])
	names = list(set(cities))  # 将城市名称去重复值，便于计算

	# 获取各个城市的岗位数量值，装在 final 列表中
	final = []
	for i in range(0, len(names)):
		final.append(0)
	for each in all:
		for each_name in range(0, len(names)):
			if each[0] == names[each_name]:
				final[each_name] += 1
				break
	'''
	热力图的绘制要利用百度的 pyecharts 库，需要提前安装
	#pip install echarts-countries-pypkg #世界地图包括中国地图大约 1.9M
	#pip install echarts-china-provinces-pypkg #中国省份地图 730k
	#pip install echarts-china-cities-pypkg #中国城市地图 3.8M
	#pip install echarts-china-counties-pypkg #中国县镇地图 4.1M
	#pip install echarts-china-misc-pypkg #中国区域划分
	'''
	# 此处需要将资料中给出的 city_coordinates.json 文件放在 python 目录下，获取各个城市的经纬度信息
	aa = [list(z) for z in zip(names, final)]
	geo = (
		Geo()
		.add_schema(maptype="china")
		.add(
			"岗位-城市数量分布热力图",  # 图题
			aa,
			type_=ChartType.HEATMAP,  # 地图类型
		)
		.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
		# 设置是否显示标签
		.set_global_opts(
			visualmap_opts=opts.VisualMapOpts(max_=260),  # 设置 legend显示的最大值
		)
	)
	geo.render("cities_heatmap.html")  # 以 html 类型保存，名称为cities_heatmap
	cursor.close()  # 关闭操作游标


def salary_xueli_boxplot():  # 主函数调用的salary_xueli_boxplot()函数
	cursor = db.cursor()
	cursor.execute("SELECT `薪资`,`工作要求` FROM after_clean")
	all = cursor.fetchall()
	# 创建两个空列表，用来存储筛选后的学历和薪资
	xueli = []
	salary = []
	for each in all:
		if each[1] != '' and each[1].split(',')[1] != '':  # 筛除学历的缺失值以及部分异常值
			xueli.append(each[1].split(',')[1])
			# 筛除薪资的缺失值
			salary.append(each[0].split('千/月')[0])
		# print(each[1].split(',')[1],"+",each[0].split('千/月')[0])
	# 对学历去重复值，并转换为列表形式，得到学历类型列表 xueli_after_quchong
	xueli_after_quchong = list(set(xueli))
	# 创建一个包含学历类型数个空列表的列表
	final = []
	for each in range(len(xueli_after_quchong)):
		final.append([])
	# 将不同类型学历的所有薪资先由字符串类型转换为浮点数类型，通过 index 索引，放进final 列表中对应的空列表，得到每种学历对应的薪资列表 final
	for each in xueli_after_quchong:
		for i in range(len(xueli)):
			if xueli[i] == each:
				final[xueli_after_quchong.index(each)].append(float(salary[i]))
	# print(final)
	# 画图
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
	plt.boxplot(final, labels=xueli_after_quchong)
	plt.title('学历-薪资水平箱线图', fontsize=15)
	plt.ylabel('薪资(单位：千/月)', fontsize=12)
	plt.show()  # 展示图形
	cursor.close()  # 关闭操作游标


def post_salary():  # 主函数调用的 post_salary()函数
	cursor = db.cursor()
	# 从数据库表中选择这 7 种职务的薪资和名称
	cursor.execute("SELECT `当前爬取岗位`,`薪资` FROM `after_clean` ")
	results = cursor.fetchall()
	# 根据实验课程大纲中的表格分类信息，将 30 种岗位分为九小类
	post = ['技术管理类', '技术开发类', '业务咨询类', '技术支持类', 'IT 运维类', '数据管理类', '数据运营类', '市场职能类', '产品运营类']
	T1 = ['产品经理', '产品助理', '交互设计']
	T2 = ['前端开发', '软件设计', 'IOS 开发', '业务分析', '安卓开发', 'PHP 开发']
	C1 = ['业务咨询', '需求分析', '流程设计']
	C2 = ['售后经理', '售前经理', '技术支持', 'ERP 实施', '实施工程师']
	C3 = ['IT 项目经理', 'IT 项目助理']
	D1 = ['信息咨询', '数据挖掘']
	D2 = ['数据运营', '数据分析']
	P1 = ['网络营销', '物流与供应链', '渠道管理']
	P2 = ['电商运营', '客户关系管理', '新媒体运营', '产品运营']
	clasify = [T1, T2, C1, C2, C3, D1, D2, P1, P2]
	post1 = []
	for each_post in post:
		for i in range(7):
			post1.append(each_post)  # 将九小类岗位重复 7 次，放进 post1 列表中，用于后续计算数值和画图
	# 薪资水平划分
	salary = ['5 千/月以下', '5-10 千/月', '10-15 千/月', '15-20 千/月', '20-25千/月', '25-30 千/月', '30 千/月以上']
	# 为了能对应九小类职务，将每种水平薪资取 7 次
	salary1 = salary * 9
	# 构建一个包含 7*9 个元素的列表，初始值为 0，用于存储职务与薪资水平的一对一岗位数量
	count = []
	for i in range(7 * 9):
		count.append(0)
	# 计算 count 列表种每个元素的值，即职务与薪资水平的一对一岗位数量
	for each_result in results:
		for i in range(9):
			if each_result[0] in clasify[i] and each_result[1] != '':
				if float(each_result[1].split('千/月')[0]) < 5:
					count[i * 7] += 1
				elif 5 <= float(each_result[1].split('千/月')[0]) < 10:
					count[i * 7 + 1] += 1
				elif 10 <= float(each_result[1].split('千/月')[0]) < 15:
					count[i * 7 + 2] += 1
				elif 15 <= float(each_result[1].split('千/月')[0]) < 20:
					count[i * 7 + 3] += 1
				elif 20 <= float(each_result[1].split('千/月')[0]) < 25:
					count[i * 7 + 4] += 1
				elif 25 <= float(each_result[1].split('千/月')[0]) < 30:
					count[i * 7 + 5] += 1
				elif 30 <= float(each_result[1].split('千/月')[0]):
					count[i * 7 + 6] += 1
	# 整理数据
	df = pd.DataFrame({
		'职位': post1,
		'薪资': salary1,
		'数量': count
	})
	# 把所有涉及到的节点去重规整到一起，即把“职位”列的'数据分析','产品经理', '产品助理', '交互设计', '前端开发', '软件设计', 'IOS 开发'和“薪资”
	# 列中的'5 千/月以下','5-10 千/月','10-15 千/月','15-20 千/月','20-25 千/月','25-30 千/月','30 千/月以上'以列表内嵌套字典的形式去重汇总
	nodes = []
	for i in range(2):
		values = df.iloc[:, i].unique()
		for value in values:
			dic = {}
			dic['name'] = value
			nodes.append(dic)
	# 定义边和流量，用 Source-target-value 字典格式，能清晰描述数据的流转情况
	linkes = []
	for i in df.values:
		dic = {}
		dic['source'] = i[0]
		dic['target'] = i[1]
		dic['value'] = i[2]
		linkes.append(dic)
	# 画图
	pic = (
		Sankey().add(
			'职位_薪资桑基图',  # 图例名称
			nodes,  # 传入节点数据
			linkes,  # 传入边和流量数据
			# 设置透明度、弯曲度
			linestyle_opt=opts.LineStyleOpts(opacity=0.3, curve=0.5),
			# 标签显示位置
			label_opts=opts.LabelOpts(position='right'),
			# 节点之间的距离
			node_gap=30,
		)
		.set_global_opts(title_opts=opts.TitleOpts(title='职位_薪资桑基图'))
	)
	pic.render('Sankey.html')  # 默认保存在本代码同文件夹下


# 用来描绘所有岗位的工作待遇热词共现
def wordcloud_welfare():  # 主函数调用的 wordcloud_welfare()函数
	cursor = db.cursor()
	cursor.execute("SELECT `工作待遇` FROM `after_clean`")
	results = cursor.fetchall()
	txt = ''
	for each_result in results:
		txt = txt + each_result[0]
	# 统计词频的字典
	word_freq = dict()
	# 装载停用词,此处需将资料中给出的 hit_stopwords.txt 文件放到本代码所在路径下
	with open("D:/Desktop/python 数据爬虫及可视化实验/实验所需输入文件/stopwords.txt", "r", encoding='utf-8') as f1:  # 读取我们的待处理本文
		txt1 = f1.readlines()
	stoplist = []
	for line in txt1:
		stoplist.append(line.strip('\n'))
	# 切分、停用词过滤、统计词频
	for w in list(jieba.cut(txt)):
		if len(w) > 1 and w not in stoplist:
			if w not in word_freq:
				word_freq[w] = 1
			else:
				word_freq[w] = word_freq[w] + 1
	# 指定背景模式图片
	back_color = imread("D:/Desktop/python 数据爬虫及可视化实验/实验所需输入文件/地大.png")
	# 构造 WordCloud 对象
	wc = WordCloud(background_color='white', max_words=100, collocations=False, width=1000, height=1000,
	               font_path='simhei.ttf', mask=back_color)
	# 调用方法生成词云图
	wc = wc.generate_from_frequencies(word_freq)
	# 保存图片
	wc.to_file('WordCloud.png')
	plt.imshow(wc)
	plt.axis("off")
	plt.show()


# 创建主函数
if __name__ == '__main__':
	gangweishuliang_hist()
	xueli_pie()
	company_size()
	gangweishuliang_heatmap()
	salary_xueli_boxplot()
	post_salary()
	wordcloud_welfare()
	db.close()
