import xlrd
import pandas as pd
from pandas import DataFrame
import re
import emoji
import pandas as pd
import xlwt as ExcelWrite

result_dic = {}
def clean_space(text):
    """"
    处理多余的空格
    """
    match_regex = re.compile(u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(should_replace_list,key=lambda i:len(i),reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()
        text = text.replace(i,new_i)
    return text

def remove_numbersign(content): #去除标签
    try:
        return re.sub(u"\\#.*?\\#|\\【.*?\\】", "", content)
    except:
        return re.sub(u"\\#.*?\\#|\\【.*?\\】", "", str(content))

def remove_content(content): #去除展开全文c 和 转发微博 和 0网页链接
    return content.replace('展开全文c',"").replace('转发微博',"").replace('O网页链接',"")

def remove_at(content): #去除@
#     return re.sub(u"\\//@.*?\\:", "", content)
    return re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", content)

def reformat(content): #去除换行和空格
    return content.replace('\n', '').replace('\r', '')
DATA_DIR = r'sentiment_analysis\\weibodata\\weibo_post.xlsx'

data = xlrd.open_workbook(DATA_DIR)
# print(data)
 
# 获取workbook中所有的表格
sheets = data.sheet_names()[::-1][1:]
print(type(sheets))
print(sheets)

for each in sheets: #table.cell(i,2).value
    list_afterclean = []
    table = data.sheet_by_name(each)
    datas = []
    for i in range(1,table.nrows):
        step1 = remove_numbersign(table.cell(i,0).value)
        step2 = remove_content(step1)
        step3 = remove_at(step2)
        step4 = reformat(step3)
        step5 = clean_space(step4)
        step6 = emoji.demojize(step5)
        list_afterclean.append(step6)
    print("reading...."+each)
    result_dic[each]=list(set(list_afterclean)) #{"date":[.....])


xls = ExcelWrite.Workbook(style_compression=2)
for each in result_dic.keys():
    sheet = xls.add_sheet(each)
    for i in range(len(result_dic[each])):
        sheet.write(i,0,result_dic[each][i])
    print("writing...."+each)
xls.save("sentiment_analysis\\weibodata\\clean_weibo_post_v2.xls")



       
# list_afterclean = list(set(list_afterclean)) #去重
# for each in list_afterclean:
#     # print(each)
#     print(" ")

# list转dataframe
# df = pd.DataFrame(list_afterclean, columns=['cleandata'])

# 保存到本地excel
# df.to_excel("D:\\VSCode\\python\\sentiment_analysis\\clean_weibo_data\\dataclean_test1.xlsx", index=False)

