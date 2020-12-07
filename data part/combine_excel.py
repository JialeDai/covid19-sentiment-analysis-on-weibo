import xlrd
import pandas as pd
from pandas import DataFrame
#  一定要是xlsx
DATA_DIR = r'/Users/david/Documents/python/.vscode/weibo/微博数据/冠状病毒.xlsx'

wb = xlrd.open_workbook(DATA_DIR)
print(wb)
 
# 获取workbook中所有的表格
sheets = wb.sheet_names()
# print(sheets)
# print(type(sheets))
 
#取日期
count_date=[]
combine_sheet = []
date_index = {}
for each in sheets:
    date = each[0:10]
    count_date.append(date)
    if date in count_date:
        combine_sheet.append(each)
#     print(combine_sheet)
#     print(count_date)

for each in count_date:
    date_index[each] = [i for i,x in enumerate(count_date) if x == each]
#     print( each,[i for i,x in enumerate(count_date) if x == each])

print(date_index)

writer = pd.ExcelWriter('/Users/david/Documents/python/.vscode/weibo/微博数据/冠状病毒4.xls')

for i in date_index: #{'2020-02-20': [0, 2, 3], '2020-02-21': [1]}
    df_combine = DataFrame()
#     print(df_combine)
    count = 0
    for each in range(len(date_index[i])):
        print('handling',combine_sheet[date_index[i][count]])
        df = pd.read_excel(DATA_DIR, sheet_name=combine_sheet[date_index[i][count]],header = 0,skiprows=0, index=False, encoding='utf8')
#         print(df)
        df_combine = df_combine.append(df)
        print(count)
        count+=1
#         print(df_combine)
    df_combine.to_excel(writer,i)
    writer.save()
#     print (i, date_index[i])

# for each in date_index: #2020-02-20 2020-02-21
#     df_combine = DataFrame()
#     count = 0
#     for i in range(len(date_index[key])):
#         print(i)
# # 循环遍历所有sheet
# df_28 = DataFrame()
# for i in range(len(sheets)):
#     df = pd.read_excel(DATA_DIR, sheet_name=i, skiprows=0, index=False, encoding='utf8')
#     df_28 = df_28.append(df)
# # 去除缺省值
# print(df_28)