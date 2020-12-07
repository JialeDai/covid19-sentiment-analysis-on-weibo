from django.shortcuts import render
import numpy as np
import pymongo
import json

def get_world():
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.nCoV_data
    world_data = db.nCoV_world_data

    infect_data = []
    for data in world_data.find():
        day_infection = {}
        time = data['date'][:4].replace('/', '.')
        day_infection['time'] = time
        
        # sort the country infect data
        country_data = data['country_data']
        sorted_country_data = sorted(country_data.items(), key=lambda item:item[1][0]['Confrimed'], reverse=True)
        temp_d = {}
        for a, b in sorted_country_data: 
            temp_d.setdefault(a, b)
        
        country_data_list = []
        countries = list(temp_d.keys())
        value_list = list(temp_d.values())
        for i in range(0, len(countries)):
            country_data_list.append({
                'name': countries[i], 
                'value': [value_list[i][0]['Confrimed']] + [value_list[i][1]['Recovered']] + [value_list[i][2]['Deaths']]
            })
        day_infection['data'] = country_data_list
        infect_data.append(day_infection)
        
    return infect_data

# Create your views here.
def index(request):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.nCoV_data

    CN_data = db.nCoV_CN_data
    results = db.results

    # get the viurs data in China
    province_list = []
    province_infection = CN_data.find({'date': '2020-02-16'})[0]['province_infection']
    for each in province_infection:
        province_list.append(each['province'])

    days_list = []
    infect_data = []
    overall_confirmed = []
    overall_death = []
    overall_recovered = []
    for data in CN_data.find():
        days_list.append(data['date'][6:11])
        
        # construct the infected data list for each province in each day
        day_infection = []
        current_provinces = {}
        for each in data['province_infection']:
            current_provinces[each['province']] = each['confirmed']
        for province in province_list:
            if province in list(current_provinces.keys()):
                day_infection.append(current_provinces[province])
            else:
                day_infection.append(0)
        infect_data.append(day_infection)
        overall_confirmed.append(data['overall'][0]['confirmed_overall'])
        overall_death.append(data['overall'][0]['dead_overall'])
        overall_recovered.append(data['overall'][0]['cured_overall'])
    for i in range(0,31):
        days_list[i] = '1' + days_list[i]
    province_list = ['上海', '云南', '内蒙古', '北京', '台湾', '吉林', '四川', '天津', '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西', '河北', '河南', '浙江', '海南', '湖北', '湖南', '澳门', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '香港', '黑龙江']

    # get the data for sentiment analysis page
    SA_data = results.find({'tag': 'sentiment_analysis'})[0]['data']
    weibo_cnt = results.find({'tag': 'weibo_count'})[0]['data']
    predictions = []
    for each in SA_data:
        predictions.append(each['day_sentiment'])
    post_days = list(weibo_cnt.keys())
    post_days = [day[5:] for day in post_days]
    post_cnt = list(weibo_cnt.values())
    # get the sentiment counts for each day
    pred_cnt = results.find({'tag': 'prediction_count'})[0]['data']
    pos_cnt, neu_cnt, neg_cnt = [], [], []
    for each in list(pred_cnt.values()):
        pos_cnt.append(each['1'])
        neu_cnt.append(each['0'])
        neg_cnt.append(each['-1'])
    # normalize the confirmed data
    av_confirmed = np.mean(overall_confirmed)
    min_confirmed = min(overall_confirmed)
    norm_confirmed = [ (x - av_confirmed) / (2*(av_confirmed - min_confirmed)) for x in overall_confirmed]
    # compute the daliy active cases 
    overall_active = [overall_confirmed[i] - overall_recovered[i] - overall_death[i] for i in range(len(overall_confirmed))]
    # get world comfirmed data 
    world_data = get_world()
    world_confirmed = []
    for day_data in world_data:
        sum_confirmed = 0
        for each in day_data['data']:
            sum_confirmed += each['value'][0]
        world_confirmed.append(sum_confirmed)
    world_confirmed = overall_confirmed[19:52] + world_confirmed

    # get the data for word cloud page
    WC_data = results.find({'tag': 'word_cloud'})[0]['data']
    word_cloud_kws = list(WC_data.keys())
    word_cloud_weights = list(WC_data.values())

    context = {
        'days_list': json.dumps(days_list),
        'province_list': json.dumps(province_list),
        'infect_data': json.dumps(infect_data),
        'overall_confirmed': json.dumps(overall_confirmed),
        'overall_death': json.dumps(overall_death),
        'overall_active': json.dumps(overall_active),
        'post_cnt': json.dumps(post_cnt),
        'predictions': json.dumps(predictions),
        'post_days': json.dumps(post_days),
        'norm_confirmed': json.dumps(norm_confirmed),
        'word_cloud_kws': json.dumps(word_cloud_kws),
        'word_cloud_weights': json.dumps(word_cloud_weights),
        'pos_cnt': json.dumps(pos_cnt),
        'neu_cnt': json.dumps(neu_cnt),
        'neg_cnt': json.dumps(neg_cnt),
        'world_confirmed': json.dumps(world_confirmed),
    }

    return render(request, 'index.html', context)


def world(request):
    infect_data = get_world()

    context = {
        'infect_data': json.dumps(infect_data),
    }

    return render(request, 'world.html', context)


def document(request):
    
    context = {

    }

    return render(request, 'document.html', context)

def key_tech(request):

    context = {

    }
    return render(request, 'key_tech.html', context)

def contact(request):

    context = {

    }
    return render(request, 'contact.html', context)
