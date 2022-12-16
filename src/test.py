each_data= ['3万及以下/年']
i=0
each_data[i] = str((float(each_data[i].split('万')[0].split('-')[0]) + float(each_data[i].split('万')[0].split('-')[1]))* 5 / 12) + '千/月'
print(each_data[i])