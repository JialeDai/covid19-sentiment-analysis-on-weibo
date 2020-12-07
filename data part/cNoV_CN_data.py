import pandas as pd
import numpy as np
import xlrd
from pymongo import MongoClient
import pymongo
from datetime import datetime

# client = pymongo.MongoClient("mongodb://DJL:Djl123456@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
# mydb=client.nCov_data

def sort_date_list(list):
    datelist=[]
    for each in list:
        each = datetime.strptime(each,"%m/%d/%Y")
        datelist.append(each)
    sorted_datelist = []
    for each in sorted(datelist):
        each= each = str(each.month)+"/"+str(each.day)+"/"+str(each.year)
        sorted_datelist.append(each)
    return sorted_datelist
province_dataframe = pd.read_excel(open('D:\\VSCode\\python\\sentiment_analysis\\offcialdata\\countrydata\\Wuhan-2019-nCoV.xlsx', 'rb'),sheet_name='省份数据')
country_dataframe = pd.read_excel(open('D:\\VSCode\\python\\sentiment_analysis\\offcialdata\\countrydata\\Wuhan-2019-nCoV.xlsx', 'rb'),sheet_name='全国数据')

province_data =  np.array(province_dataframe).tolist()
country_data = np.array(country_dataframe).tolist()


province_datelist = []
list1 = province_dataframe['date'].tolist()
for i in list1:
    if i not in province_datelist:
        province_datelist.append(i)
# province_datelist = sort_date_list(province_datelist)
province_datelist = province_datelist
# print(province_datelist)
province_datalist = []
# print(province_data)

for each in province_datelist:
    date = each
    dic_unit = {}
    dic_unit['date'] = str(each)
    daily_province_data = []
    daily_overall_data = []

    for sublist_overall in country_data:
        subdic = {}
        if date in sublist_overall:
            subdic['confirmed_overall'] = sublist_overall[1]
            subdic['suspected_overall'] = sublist_overall[2]
            subdic['cured_overall'] = sublist_overall[3]
            subdic['dead_overall'] = sublist_overall[4]
            daily_overall_data.append(subdic)
        else:
            pass

    for sublist in  province_data:
        subdic = {}
        if date in sublist:
            subdic['province'] = sublist[1]
            subdic['confirmed'] = sublist[2]
            subdic['suspected'] = sublist[3]
            subdic['cured'] = sublist[4]
            subdic['dead'] = sublist[5]
            daily_province_data.append(subdic)
            # print(date,sublist,daily_province_data)
        else:
            pass
    
    dic_unit['province_infection'] = daily_province_data
    dic_unit['overall'] = daily_overall_data
    province_datalist.append(dic_unit)

client = pymongo.MongoClient("mongodb://DJL:Djl123456@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
mydb = client.nCoV_data
province_datalist = province_datalist[0:-2]
tmp_list = []
for each in province_datalist:
    tmp_dic = {}
    tmp_dic["date"]=each['date'][0:10]
    tmp_dic["province_infection"] = each["province_infection"]
    tmp_dic["overall"] = each['overall']
    tmp_list.append(tmp_dic)
# print(tmp_list[0])

big_dict = {}
for each in tmp_list:
    key = datetime.strptime(each["date"],"%Y-%m-%d")
    big_dict[key]=each

# print(sorted(big_dict.keys()))
final_list = []
# for each in sorted(big_dict.keys()):
#     final_list.append(big_dict[each])

# print(final_list[0])
final_list = sorted(big_dict.items(),key=lambda x:x[0])
for each in sorted(big_dict.items(),key=lambda x:x[0]):
    final_list.append(each[1])
    # print(type(each[1]))
# print(type(final_list))


mycol = mydb['nCoV_CN_data']

for each in final_list:
    try:
        mycol.insert_one(each[1])
        print("insert..."+ each[1]['date'])
    except:
        print("!!!!!!!!!failed!!!!!!!!!!!!!")

# print(province_datalist)
# for each in final_list:
#     try:
#         mycol.insert_one(each)
#     except:
#         print("insert failed")
#     # print(each)

# mycol.insert_many(list(final_list))
