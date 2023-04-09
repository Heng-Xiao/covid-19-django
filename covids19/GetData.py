#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author YangLuLu
# @date 2022/1/21
# @file GetData.py
'''
专用于爬取疫情数据
目前已经无用
'''
from covids19.connect import connect
import jieba.analyse
import jsonpath
import time
import pandas as pd
import requests
from lxml import etree
import json
import datetime

url = 'http://api.tianapi.com/ncov/index?key=95905271a4bb4ebed85e34369f076013'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
resp = requests.post(url)
data = json.loads(resp.text)


# 获取新闻信息
def get_news():
    title = jsonpath.jsonpath(data, "$..title")
    infoSource = jsonpath.jsonpath(data, "$..infoSource")
    summary = jsonpath.jsonpath(data, "$..summary")
    pubDate = jsonpath.jsonpath(data, "$..pubDate")
    newtime = []
    for i in pubDate:
        newtime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i / 1000))))
    news = pd.DataFrame(
        {'news_title': title, 'publish_time': newtime, 'news_summary': summary, 'news_source': infoSource})
    # create_engine('mysql+pymysql://用户名:密码@主机/库名?charset=utf8')
    # 将数据写入sql
    return news

def get_news_value():
    conn = connect()
    sql = """ select news_summary from news ORDER BY publish_time DESC LIMIT 5"""
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = cur.fetchall()
    str1 = ""
    for i in data1:
        p = str(i).replace('年', '1').replace('月', '2').replace('日', '3')
        str1 += str(p)
    import re
    temp = re.sub('[\d]', '', str1)  # [0-9]
    word = jieba.analyse.extract_tags(temp, topK=70, withWeight=True,allowPOS=('ns','n'))
    name = []
    value = []
    for i in range(0,len(word)):
        name.append(word[i][0])
        value.append(word[i][1])
    news_value = pd.DataFrame(
        {'name': name, 'value': value})
    return news_value

# 获取风险地区名称
def get_risk_areas():
    mid = jsonpath.jsonpath(data, "$..mid")
    high = jsonpath.jsonpath(data, "$..high")
    areas_name = []
    areas_degree = []
    for i in high[0]:
        areas_name.append(i)
        areas_degree.append('高风险地区')
    for i in mid[0]:
        areas_name.append(i)
        areas_degree.append('中风险地区')
    risk_areas = pd.DataFrame({'areas_name': areas_name, 'areas_degree': areas_degree})
    # 将数据写入sql

    return risk_areas


# 获取中国总共确诊的信息
def get_china_total():
    currentConfirmedCount = jsonpath.jsonpath(data, "$..currentConfirmedCount")[0]  # 现存确诊人数
    confirmedCount = jsonpath.jsonpath(data, "$..confirmedCount")[0]  # 累计确诊人数
    suspectedCount = jsonpath.jsonpath(data, "$..suspectedCount")[0]  # 累计境外输入人数
    curedCount = jsonpath.jsonpath(data, "$..curedCount")[0]  # 累计治愈人数
    deadCount = jsonpath.jsonpath(data, "$..deadCount")[0]  # 累计死亡人数
    seriousCount = jsonpath.jsonpath(data, "$..seriousCount")[0]  # 现存无症状人数
    suspectedIncr = jsonpath.jsonpath(data, "$..suspectedIncr")[0]  # 新增境外输入人数
    now = datetime.datetime.now()
    nowtime = now.strftime("%Y-%m-%d %H:%M:%S")
    china_total = pd.DataFrame({'nowtime': [nowtime], 'currentConfirmedCount': [currentConfirmedCount],
                                'confirmedCount': [confirmedCount], 'suspectedCount': [suspectedCount],
                                'curedCount': [curedCount], 'deadCount': [deadCount], 'seriousCount': [seriousCount],
                                'suspectedIncr': [suspectedIncr]})
    # 将数据写入sql
    # pd.io.sql.to_sql(china_total, 'china_total', con=engine, if_exists='append', index=None)
    return china_total
def get_china_total_forqq():
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf'
    resp = requests.post(url)
    data = json.loads(resp.text)
    data = data['data']
    now = datetime.datetime.now()
    nowtime = now.strftime("%Y-%m-%d %H:%M:%S")
    confirm = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..confirm")
    nowConfirm = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..nowConfirm")
    importedCase = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..importedCase")
    dead = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..dead")
    heal = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..heal")
    noInfect = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..noInfect")
    local_acc_confirm = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..local_acc_confirm")
    nowSevere = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..nowSevere")
    suspect = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..suspect")
    showLocalConfirm = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..showLocalConfirm")
    showlocalinfeciton = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..showlocalinfeciton")
    noInfectH5 = jsonpath.jsonpath(data['diseaseh5Shelf']['chinaTotal'], "$..noInfectH5")
    chain_total_forqq = pd.DataFrame(
        {'nowtime':nowtime,'confirm': confirm, 'nowConfirm': nowConfirm, 'importedCase': importedCase, 'dead': dead,
         'heal': heal, 'noInfect': noInfect, 'local_acc_confirm': local_acc_confirm, 'suspect': suspect,
         'nowSevere': nowSevere, 'showLocalConfirm': showLocalConfirm,
         'showlocalinfeciton': showlocalinfeciton, 'noInfectH5': noInfectH5})
    return chain_total_forqq

#爬取的网址（百度疫情）
#获取当日省份信息
def get_areaTotal():
    url="https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3"
    #伪装请求头
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    #获取网页地址
    response=requests.get(url,timeout=30,headers=headers)
    #解析数据内容
    html=etree.HTML(response.text)
    #在网页中寻找我们想要的数据（可以找到对应标签右键复制xpath）
    result=html.xpath('//*[@id="captain-config"]/text()')
    result=json.loads(result[0])
    result_in=result["component"][0]["caseList"]
    # (['省份','累计确诊','死亡','治愈','新增确诊','现有确诊'
    #            '累计确诊增量','死亡增量','治愈的增量','现有确诊增量'])
    areaTotal = pd.DataFrame(columns=['area','confirmed','died','crued','confirmedRelative','curConfirm',
                               'curedRelative','asymptomaticRelative','asymptomatic',
                               'nativeRelative'])
    # name = 'area_'+ time.strftime("%Y%m%d",time.localtime(time.time()))
    for each in result_in:
        temp_list = [each['area'], each['confirmed'], each['died'], each['crued'],
                     each['confirmedRelative'], each['curConfirm'], each['curedRelative'],
                     each['asymptomaticRelative'], each['asymptomatic'],
                     each['nativeRelative']]
        areaTotal1 = pd.DataFrame(temp_list).T
        areaTotal1.columns = areaTotal.columns
        areaTotal = pd.concat([areaTotal, areaTotal1], axis=0, ignore_index=True)
#     pd.io.sql.to_sql(df,name,con = engine ,if_exists = 'replace',index=None)
    return areaTotal

def get_area_history_confirm():
    areaname = ['西藏','澳门','青海','台湾','香港','贵州','吉林','新疆','宁夏','内蒙古','甘肃','天津','山西','辽宁',
                '黑龙江','海南','河北','陕西','云南','广西','福建','上海','北京','江苏','四川','山东','江西','重庆',
                '安徽','湖南','河南','广东','浙江','湖北']
    all_data = {}
    # header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
    for c in areaname:
        history_url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={0}'.format(c)
        resp = requests.post(history_url, headers=header)
        data3 = json.loads(resp.text)['data']
        all_data[c] = data3
    area_history_confirm = pd.DataFrame(columns=areaname)
    for c in areaname:
        area_data = all_data[c]
        confirm = jsonpath.jsonpath(area_data, "$..confirm")
        confirm = confirm[-620:]
        area_history_confirm[c] = confirm
    # 处理时间
    year = jsonpath.jsonpath(all_data['西藏'], "$..year")[-620:]
    date = jsonpath.jsonpath(all_data['西藏'], "$..date")[-620:]
    yeardate = []
    for i in range(len(year)):
        date1 = str(year[i]) + date[i]
        date1 = date1.replace(".", '')
        date1 = datetime.datetime.strptime(date1, '%Y%m%d')
        yeardate.append(date1)
    area_history_confirm.insert(0, 'yeardate', yeardate)
    return area_history_confirm
def get_area_history_confirm_add():
    areaname = ['西藏','澳门','青海','台湾','香港','贵州','吉林','新疆','宁夏','内蒙古','甘肃','天津','山西','辽宁',
                '黑龙江','海南','河北','陕西','云南','广西','福建','上海','北京','江苏','四川','山东','江西','重庆',
                '安徽','湖南','河南','广东','浙江','湖北']
    all_data = {}
    # header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
    for c in areaname:
        history_url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={0}'.format(c)
        resp = requests.post(history_url, headers=header)
        data3 = json.loads(resp.text)['data']
        all_data[c] = data3
    area_history_confirm_add = pd.DataFrame(columns=areaname)
    for c in areaname:
        area_data = all_data[c]
        confirm_add = jsonpath.jsonpath(area_data, "$..confirm_add")
        confirm_add = confirm_add[-620:]
        area_history_confirm_add[c] = confirm_add
    # 处理时间
    year = jsonpath.jsonpath(all_data['西藏'], "$..year")[-620:]
    date = jsonpath.jsonpath(all_data['西藏'], "$..date")[-620:]
    yeardate = []
    for i in range(len(year)):
        date1 = str(year[i]) + date[i]
        date1 = date1.replace(".", '')
        date1 = datetime.datetime.strptime(date1, '%Y%m%d')
        yeardate.append(date1)
    area_history_confirm_add.insert(0, 'yeardate', yeardate)
    return area_history_confirm_add
def get_chinadata():
    url = '''https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'''
    resp = requests.post(url)
    data = json.loads(resp.text)
    data = data['data']
    return data

def get_chinaDayAdd():
    data = get_chinadata()
    y = jsonpath.jsonpath(data['chinaDayAddList'],"$..y")#年
    date = jsonpath.jsonpath(data['chinaDayAddList'],"$..date")#日
    importedCase = jsonpath.jsonpath(data['chinaDayAddList'],"$..importedCase")#新增境外输入
    localConfirmadd = jsonpath.jsonpath(data['chinaDayAddList'],"$..localConfirmadd")#新增本土确诊
    infect = jsonpath.jsonpath(data['chinaDayAddList'],"$..infect")#无症状感染
    localinfectionadd = jsonpath.jsonpath(data['chinaDayAddList'],"$..localinfectionadd")#局部感染
    healRate = jsonpath.jsonpath(data['chinaDayAddList'],"$..healRate")#治愈率
    deadRate = jsonpath.jsonpath(data['chinaDayAddList'],"$..deadRate")#死亡率
    confirm = jsonpath.jsonpath(data['chinaDayAddList'],"$..confirm")#新增确诊
    suspect = jsonpath.jsonpath(data['chinaDayAddList'],"$..suspect")#新增怀疑
    heal = jsonpath.jsonpath(data['chinaDayAddList'],"$..heal")#治愈
    dead = jsonpath.jsonpath(data['chinaDayAddList'],"$..dead")#死亡
    yeardate=[]
    for i in range(len(date)):
        date1 = str(y[i])+ date[i]
        date1 = date1.replace(".", '')
        date1 = datetime.datetime.strptime(date1,'%Y%m%d')
        yeardate.append(date1)
    chinaDayAdd = pd.DataFrame({'yeardate':yeardate,'importedCase':importedCase,'localConfirmadd':localConfirmadd,
                                'infect':infect,'localinfectionadd':localinfectionadd,'healRate':healRate,
                                'deadRate':deadRate,'confirm':confirm,'suspect':suspect,'heal':heal,'dead':dead})
    return chinaDayAdd

def get_chinaDay():
    data = get_chinadata()
    y = jsonpath.jsonpath(data['chinaDayList'],"$..y")#年
    date = jsonpath.jsonpath(data['chinaDayList'],"$..date")#日
    importedCase = jsonpath.jsonpath(data['chinaDayList'],"$..importedCase")#新增境外输入
    healRate = jsonpath.jsonpath(data['chinaDayList'],"$..healRate")#治愈率
    deadRate = jsonpath.jsonpath(data['chinaDayList'],"$..deadRate")#死亡率
    confirm = jsonpath.jsonpath(data['chinaDayList'],"$..confirm")#确诊
    suspect = jsonpath.jsonpath(data['chinaDayList'],"$..suspect")#怀疑
    heal = jsonpath.jsonpath(data['chinaDayList'],"$..heal")#治愈
    dead = jsonpath.jsonpath(data['chinaDayList'],"$..dead")#死亡
    nowSevere = jsonpath.jsonpath(data['chinaDayList'],"$..nowSevere")#重症
    noInfect = jsonpath.jsonpath(data['chinaDayList'],"$..noInfect")#无症状感染
    localConfirm = jsonpath.jsonpath(data['chinaDayList'],"$..localConfirm")#本土确诊案例
    noInfectH5 = jsonpath.jsonpath(data['chinaDayList'],"$..noInfectH5")#无感染H5
    localConfirmH5 = jsonpath.jsonpath(data['chinaDayList'],"$..localConfirmH5")#本土确诊案例h5
    local_acc_confirm = jsonpath.jsonpath(data['chinaDayList'],"$..local_acc_confirm")#本土确诊案例
    nowConfirm = jsonpath.jsonpath(data['chinaDayList'],"$..nowConfirm")#现在确诊
    yeardate=[]
    for i in range(len(y)):
        date1 = str(y[i] )+ date[i]
        date1 = date1.replace(".", '')
        date1 = datetime.datetime.strptime(date1,'%Y%m%d')
        yeardate.append(date1)

    chinaDay = pd.DataFrame({'yeardate':yeardate,'importedCase':importedCase,
                        'healRate':healRate,'deadRate':deadRate,'confirm':confirm,'suspect':suspect,'heal':heal,'dead':dead,
                           'nowSevere':nowSevere,'noInfect':noInfect,'localConfirm':localConfirm,'noInfectH5':noInfectH5,
                             'localConfirmH5':localConfirmH5,'local_acc_confirm':local_acc_confirm,'nowConfirm':nowConfirm })
    return chinaDay








