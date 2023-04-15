
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from covids19.connect import connect
from covids19.SaveMysqlData import  *
from covids19.indexdata import get_context
conn = connect()#连接数据库
#登录逻辑处理
def do_login(request):
    username = request.POST["username"]#获取到用户名
    password = request.POST.get("password")#获取到密码
    sql = """SELECT * FROM user_info where username = %s"""
    cur = conn.cursor()
    cur.execute(sql, username)#执行sql语句
    data = cur.fetchall()
    if len(data) == 1:#用户名正确，校验成功
        sql1 = """SELECT * FROM user_info where username = %s and password = %s"""
        cur.execute(sql1, (username, password))  # 执行sql语句
        data1 = cur.fetchall()
        if len(data1) == 1:
            return redirect("/index")#重定向url回大屏
        if len(data1) == 0:
            return render(request, "login.html", context={"error": "密码错误！请重新登录"})
    if len(data) == 0:
        return render(request, "login.html", context={"error": "用户名不存在"})

def login(request):
    return render(request, "login.html")
#更新数据处理逻辑
def update(request):
    save_area_history_confirm()  # 各省份历史累计确诊数据
    save_area_history_confirm_add()  # 各省份历史新增确诊数据
    save_news()  # 最新新闻表
    save_china_total_forqq()  # 中国总数据来自腾讯疫情网
    save_areaToday()  # 当日各省份总数据
    save_risk_areas()  # 风险地区数据
    save_chinaDayAdd()  # 中国每日新增历史数据
    save_chinaDay()  # 中国每日累计历史数据
    return HttpResponseRedirect("/index")#重定向回可视化大屏页面
#注册逻辑处理
def do_register(request):
    username = request.POST["username"]#获取用户输入的用户名
    password = request.POST.get("password")#获取用户输入的用户密码
    print("用户名和密码分别是：", username, password)
    sql = """SELECT * FROM user_info where username = %s"""#根据用户名查找用户信息
    cur = conn.cursor()
    cur.execute(sql, (username))#执行sql语句
    data = cur.fetchall()
    if len(data) == 1:#用户名已存在！注册失败
        return render(request, "register.html", context={"error": "用户名已存在"})
    if len(data) == 0:#无相同用户名可注册
        # 将用户输入的用户名和密码插入到数据库中的user_info表中的sql语句
        sql1 = "INSERT INTO user_info(username, password) VALUES(%s, %s);"
        cur.execute(sql1, (username, password))  # 执行sql语句
        cur.connection.commit()
        data1 = cur.fetchall()
        return HttpResponseRedirect("/index")#注册成功重定向回登录页面
def register(request):
    return render(request, "register.html")

