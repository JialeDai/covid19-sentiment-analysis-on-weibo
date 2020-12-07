import xlrd
import pymongo
DATA_DIR = r"D:\\VSCode\\python\\sentiment_analysis\\weibodata\\weibo_post.xlsx"
data = xlrd.open_workbook(DATA_DIR)
sheets = data.sheet_names()[0:-1][::-1]
result = []
weibo_post_data = {}
weibo_post={}
weibo_post_clean={}
for each in sheets:
    print('counting(raw) ..... ' + each)
    table = data.sheet_by_name(each)
    weibo_post_data[each] = table.nrows

weibo_post["tag"]="weibo_count"
weibo_post['data']=weibo_post_data
# print(weibo_post)

DTAT_DIR_CLEAN = r"D:\\VSCode\\python\\sentiment_analysis\\weibodata\\clean_weibo_post_v2.xls"
data_clean = xlrd.open_workbook(DTAT_DIR_CLEAN)
sheets_clean = data_clean.sheet_names()
weibo_post_data_clean = {}
for each in sheets_clean:
    print('counting(clean) ..... ' + each)
    table=data_clean.sheet_by_name(each)
    weibo_post_data_clean[each]=table.nrows

weibo_post_clean["tag"]="weibo_clean_count"
weibo_post_clean["data"] = weibo_post_data_clean
# print(weibo_post_clean)

result.append(weibo_post)
result.append(weibo_post_clean)
client = pymongo.MongoClient("mongodb://DJL:Djl123456@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
mydb = client.nCoV_data
mycol = mydb["results"]
for each in result:
    print("insert========")
    mycol.insert_one(each)