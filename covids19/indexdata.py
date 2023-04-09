from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from pymysql import Connect
import pandas as pd
import json
import jieba.analyse
from covids19.connect import connect
from numpy import *
conn = connect()
#仪表盘
def get_dead_rate():
    sql = """SELECT nowtime,confirm,dead FROM `china_total_forqq` order by nowtime desc limit 1 """
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    confirmedCount = data[0][1]
    deadCount = data[0][2]
    dead_rate = round(round(deadCount / confirmedCount, 4) * 100, 2)  # 死亡率
    return dead_rate
def get_news():
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
    word1 = []
    for i in word:
        name = ["name"]
        value = ["value"]
        a = [i[0]]
        b = [i[1]]
        c = dict(zip(name, a))  # 列表合并为键值对
        d = dict(zip(value, b))
        e = {}
        e.update(c)  # 键值对加入字典
        e.update(d)
        word1.append(e)
    return word1


def china_total():
    sql = """SELECT nowtime,confirmedCount,currentConfirmedCount,suspectedCount,deadCount FROM `china_total` order by nowtime desc limit 1 """
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    confirmedCount = data[0][1]
    currentConfirmedCount = data[0][2]
    suspectedCount = data[0][3]
    deadCount = data[0][4]
    return confirmedCount,currentConfirmedCount,suspectedCount,deadCount
def china_total_forqq():
    sql = """SELECT nowtime,confirm,nowConfirm,importedCase,dead FROM `china_total_forqq` order by nowtime desc limit 1"""
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    confirmedCount = data[0][1]
    currentConfirmedCount = data[0][2]
    suspectedCount = data[0][3]
    deadCount = data[0][4]
    return confirmedCount,currentConfirmedCount,suspectedCount,deadCount
def get_riskAreas():
    sql = """ SELECT * FROM `risk_areas`"""
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = cur.fetchall()
    data2 = []
    data3 = []
    for i in data1:
        data2.append(i[0])
        data3.append(i[1])
    a = dict(zip(data2, data3))
    return a
def get_ChinaDayAddImportedCaseAndConfirm():
    cur = conn.cursor()
    cur.execute(
        "SELECT yeardate,importedCase,localConfirmadd FROM `china_day_add`")
    result = cur.fetchall()
    year = []
    importedCase = []  # 新增境外输入
    localConfirmadd = []  # 新增确诊
    for i in result:
        year.append(str(i[0])[0:10])
        importedCase.append(i[1])
        localConfirmadd.append(i[2])
    return year,importedCase,localConfirmadd
def get_mapData():
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM `area_history_confirm`  ORDER BY yeardate DESC LIMIT 365")
    result = cur.fetchall()
    data = pd.DataFrame(list(result)).iloc[::-1]
    year = []
    areaname = ['西藏', '澳门', '青海', '台湾', '香港', '贵州', '吉林', '新疆', '宁夏', '内蒙古', '甘肃', '天津', '山西', '辽宁',
                '黑龙江', '海南', '河北', '陕西', '云南', '广西', '福建', '上海', '北京', '江苏', '四川', '山东', '江西', '重庆',
                '安徽', '湖南', '河南', '广东', '浙江', '湖北']
    for i in data[0]:
        year.append(str(i)[0:10])
    del data[0]
    b = []
    for i in range(len(data)):
        a = []
        for j in data.iloc[i]:
            a.append(j)
        b.append(a)
    return areaname,b,year
def get_chinaNumberTotalByDay():
    cur = conn.cursor()
    cur.execute(
        "SELECT yeardate,confirm,heal,dead,nowConfirm FROM `china_day`")
    result = cur.fetchall()
    len(result)
    yeardate = []
    confirm = []
    heal = []
    dead = []
    nowConfirm = []
    for i in result:
        yeardate.append(str(i[0])[0:10])
        confirm.append(i[1])
        heal.append(i[2])
        dead.append(i[3])
        nowConfirm.append(i[4])
    return yeardate,confirm,dead,heal,nowConfirm
def get_cityrateAndConfirmed():
    cur = conn.cursor()
    cur.execute(
        "SELECT area,confirmed FROM `area_today`")
    result = cur.fetchall()
    cur1 = conn.cursor()
    cur1.execute(
        "SELECT areaname,cityrate FROM `area_with_various_data`")
    result1 = cur1.fetchall()
    nameAndConfirmed = []
    confirmedAvg = []
    for i in range(len(result)):
        a = {"name":result[i][0],"value":int(result[i][1])}
        nameAndConfirmed.append(a)
    cityrate = []
    for i in range(len(result1)):
        a = {"name":result1[i][0],"value":int(result1[i][1])}
        cityrate.append(a)
    cityrateAndConfirmed= []
    for i in range(len(cityrate)):
        for j in range(len(nameAndConfirmed)):
            if (cityrate[i]['name'] == nameAndConfirmed[j]['name'] and cityrate[i]['name'] != "湖北"):
                d = {"name":cityrate[i]['name'],"value":[nameAndConfirmed[j]['value'],cityrate[i]['value']]}
                cityrateAndConfirmed.append(d)
                confirmedAvg.append(int(nameAndConfirmed[j]['value']))
    confirmedAvg = round(mean(confirmedAvg), 2)
    return confirmedAvg,cityrateAndConfirmed
def get_gdpAndConfirmed():
    cur = conn.cursor()
    cur.execute(
        "SELECT area,confirmed FROM `area_today`")
    result = cur.fetchall()
    cur1 = conn.cursor()
    cur1.execute(
        "SELECT areaname,gdp FROM `area_with_various_data`")
    result1 = cur1.fetchall()
    nameAndConfirmed = []
    for i in range(len(result)):
        a = {"name":result[i][0],"value":int(result[i][1])}
        nameAndConfirmed.append(a)
    gdp = []
    for i in range(len(result1)):
        a = {"name":result1[i][0],"value":int(result1[i][1])}
        gdp.append(a)
    gdpAndConfirmed= []
    for i in range(len(gdp)):
        for j in range(len(nameAndConfirmed)):
            if (gdp[i]['name'] == nameAndConfirmed[j]['name'] and gdp[i]['name'] != "湖北"):
                d = {"name":gdp[i]['name'],"value":[nameAndConfirmed[j]['value'],gdp[i]['value']]}
                gdpAndConfirmed.append(d)
    return gdpAndConfirmed
def get_studentsInSchoolAndConfirmed():
    cur = conn.cursor()
    cur.execute(
        "SELECT area,confirmed FROM `area_today`")
    result = cur.fetchall()
    cur1 = conn.cursor()
    cur1.execute(
        "SELECT areaname,students FROM `area_with_various_data`")
    result1 = cur1.fetchall()
    nameAndConfirmed = []
    for i in range(len(result)):
        a = {"name":result[i][0],"value":int(result[i][1])}
        nameAndConfirmed.append(a)
    studentsInSchool = []
    for i in range(len(result1)):
        a = {"name":result1[i][0],"value":int(result1[i][1])}
        studentsInSchool.append(a)
    studentsInSchoolAndConfirmed= []
    for i in range(len(studentsInSchool)):
        for j in range(len(nameAndConfirmed)):
            if (studentsInSchool[i]['name'] == nameAndConfirmed[j]['name'] and studentsInSchool[i]['name'] != "湖北"):
                d = {"name":studentsInSchool[i]['name'],"value":[nameAndConfirmed[j]['value'],studentsInSchool[i]['value']]}
                studentsInSchoolAndConfirmed.append(d)
    return studentsInSchoolAndConfirmed
def get_doctorNum():
    cur = conn.cursor()
    cur.execute(
        "SELECT areaname,doctor FROM `area_with_various_data`")
    result = cur.fetchall()
    areaname = []
    doctor = []
    for i in result:
        areaname.append(i[0])
        doctor.append(i[1])
    return areaname,doctor
def get_confirmAddlist():
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM `area_history_confirm_add` ORDER BY yeardate DESC LIMIT 365")
    result = cur.fetchall()
    data = pd.DataFrame(list(result)).iloc[::-1]
    year = []
    areaname = ['西藏', '澳门', '青海', '台湾', '香港', '贵州', '吉林', '新疆', '宁夏', '内蒙古', '甘肃', '天津', '山西', '辽宁',
                '黑龙江', '海南', '河北', '陕西', '云南', '广西', '福建', '上海', '北京', '江苏', '四川', '山东', '江西', '重庆',
                '安徽', '湖南', '河南', '广东', '浙江', '湖北']
    for i in data[0]:
        year.append(str(i)[0:10])
    del data[0]
    confirmAddlist = []
    for i in data:
        confirmAddlist.append(list(map(int, list(data[i]))))
    return year, areaname, confirmAddlist
def get_pieData():
    cur = conn.cursor()
    cur.execute(
        "SELECT area,confirmed FROM `area_today`")
    result = cur.fetchall()
    areasum = 0
    areadata = []
    hubaiAndOtherData = []
    for i in result:
        if (i[0] == "台湾"):
            hubaiAndOtherData.append({"name": i[0], "value": int(i[1])})
        elif (i[0] == "香港"):
            hubaiAndOtherData.append({"name": i[0], "value": int(i[1])})
        elif (i[0] == "湖北"):
            hubaiAndOtherData.append({"name": i[0], "value": int(i[1])})
        elif (i[0] == "上海"):
            hubaiAndOtherData.append({"name": i[0], "value": int(i[1])})
        elif (i[0] == "吉林"):
            hubaiAndOtherData.append({"name": i[0], "value": int(i[1])})
        else:
            areasum = areasum + int(i[1])
            areadata.append({"name": i[0], "value": int(i[1])})
    hubaiAndOtherData.append({"name": "其他省份", "value": areasum})
    return areadata,hubaiAndOtherData
def get_context():
    dead_rate = get_dead_rate()
    newsData = get_news()
    confirmedCount, currentConfirmedCount, suspectedCount, deadCount = china_total_forqq()
    riskAreas = get_riskAreas()
    year, importedCase, localConfirmadd = get_ChinaDayAddImportedCaseAndConfirm()
    areaname, b, map_year = get_mapData()
    yeardate, confirm, dead,heal, nowConfirm = get_chinaNumberTotalByDay()
    confirmedAvg, cityrateAndConfirmed = get_cityrateAndConfirmed()
    gdpAndConfirmed = get_gdpAndConfirmed()
    studentsInSchoolAndConfirmed = get_studentsInSchoolAndConfirmed()
    areaname1, doctor = get_doctorNum()
    yearConfirmAdd, areanameConfirmAdd, confirmAddlist = get_confirmAddlist()
    areadata, hubaiAndOtherData = get_pieData()
    maskImagesrc = '''data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAMAAACahl6sAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAGUExURUxpcQMAAJgaH0QAAAABdFJOUwBA5thmAAABz0lEQVR42u3cQVLDUBADUen+l2bDhgUph+h7xqL7AKN62UFiS0RERERERERERERERESPzD8LHh1UfG7JXvtE8cl69lqA8af17LUY493t8Lkg463t8Lm04+p29toJxrXt8Lkzjgvb9ozEjkqc/lzOOV5uh8+ddbyYDp877fh12lMQOyqxhyR2VGIPSeyoxJ6SZCH2lMTRaY9B7Oi2xySOSuwpiaPTfjbEh67d7vCZawMQR495zvG93QKx5yTR7UGIk9vugDh7bBDiQYiBLJO0QAwEyBkJkGUQAwHyHyEGAgQIECBAgAABAgQIf48A4b8oQJ7u6IHw/cg2R893iGpx9EDU4uiBqMWxUtICGfyV6QrHOkkLZO638XscmySTD5BscmyRzD0sts+xQTL5IOJGx7Rk8mHdrY5BieK1OGYkUoVEx2px3CrR4VocN0l0Sy2O4xLdWAnjJEWqkGikFkecosFKGEmK1CHRhkoYAYpUIdGqWhwafN/UDolUIdHWWhz59zk+QiJ1SKQOidQhkTokUoVEz6nFoRbHgbeZ75NIHRKpQyJ1SKQOidQhkTokArJLInVIpA6JgOySqAQilUhaICoJCBERERERERERERG93Rf5Gjg4VlYsigAAAABJRU5ErkJggg=='''
    context = {'importedCase': importedCase, 'year': year,'localConfirmadd':localConfirmadd,
               'rate': dead_rate,    'cy': newsData,
               'province':areaname,'data':b,'dateChange':map_year,
                'confirmedCount': confirmedCount, 'currentConfirmedCount': currentConfirmedCount,
               'suspectedCount': suspectedCount, 'deadCount': deadCount,'riskAreas':riskAreas,
               'confirmedAvg':confirmedAvg,'cityrateAndConfirmed':cityrateAndConfirmed,'gdpAndConfirmed':gdpAndConfirmed,
                'studentsInSchoolAndConfirmed':studentsInSchoolAndConfirmed,'areaname1':areaname1,'doctor':doctor,
               'yearConfirmAdd':yearConfirmAdd,'areanameConfirmAdd':areanameConfirmAdd,'confirmAddlist':confirmAddlist,
               'areadata':areadata,'hubaiAndOtherData':hubaiAndOtherData,
               'yeardate':yeardate,'confirm':confirm,'dead':dead,'heal':heal,'nowConfirm':nowConfirm,
               'maskImagesrc':maskImagesrc
               }
    return context
def index(request):
    context = get_context()
    return render(request, 'index.html', context=context)
