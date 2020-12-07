import pandas as pd
import numpy as np 
import pymongo
from datetime import datetime


time_list=[]
result_list=[]

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
    
raw_data = pd.read_csv(open("D:\\VSCode\\python\\sentiment_analysis\\worldwidedata\\countries-aggregated.csv"))
raw_data_tolist = np.array(raw_data).tolist()

for each in raw_data_tolist:
    time_list.append(each[0])

time_list = sorted(list(set(time_list)))
time_list = sort_date_list(time_list)
print(time_list)


for date in time_list:
    world_data_dict={}
    country_data_dict={}
    for each in raw_data_tolist:
        if date == each[0]:
            country_data_dict[each[1]]=[{"Confrimed":each[2]},{"Recovered":each[3]},{"Deaths":each[4]}]    
    world_data_dict["date"]=date
    world_data_dict["country_data"]=country_data_dict
    result_list.append(world_data_dict)


client = pymongo.MongoClient("mongodb://DJL:Djl123456@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
mydb = client.nCoV_data
mycol = mydb['nCoV_world_data']

for each in result_list:
    mycol.insert_one(each)