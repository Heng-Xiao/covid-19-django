# COVID-19-Django

[![img](https://img.shields.io/badge/python-%3E=3.8.x-green.svg)](https://python.org/)  [![PyPI - Django Version badge](https://img.shields.io/badge/django%20versions-4.1-blue)](https://docs.djangoproject.com/zh-hans/4.1/) [![img](https://img.shields.io/badge/Echats-%3E%3D%204.2.1-brightgreen)](https://echarts.apache.org/zh/index.html) 

[English](./README.en.md) | [预 览](http://www.henglulu.top) | [官网文档](https://www.django-vue-admin.com) | [群聊](https://qm.qq.com/cgi-bin/qm/qr?k=fOdnHhC8DJlRHGYSnyhoB8P5rgogA6Vs&jump_from=webapi) | [Github](https://github.com/liqianglog/django-vue-admin) 

![输入图片说明](http://rt5c1mogb.hn-bkt.clouddn.com/covid/1.png)

[2022-06-27-230031.png](https://postimg.cc/4mMRhHjx)
[![2022-06-27-230031.png](https://i.postimg.cc/4x4fqz5V/2022-06-27-230031.png)](https://postimg.cc/4mMRhHjx)


💡 **「关于」**

我们是一群热爱代码的青年，在这个炙热的时代下，我们希望静下心来通过Code带来一点我们的色彩和颜色。

因为热爱，所以拥抱未来

## 平台简介

[COVID-19-Django](https://gitee.com/Heng-Xiao/covid-19-django) 国内疫情大数据可视化平台主要是为了更直观地实时关注和掌握新型冠状病毒感染的肺炎疫情防控进展，也更直观地了解全国的疫情情况，及时有效做出防控措施，在数据可视化技术的解决下，数据信息所面向的不仅是决策者，也能向大众进行授权展示，我们可以通过大数据可视化，可以更清楚、更直观地了解到目前疫情全国各地的感染人数，以此了解疫情的变化的趋势。

本系统采用Django架构开发web应用，使用Echarts绘制基本图表，利用Python语言中的requests库从一些新闻网站上爬取疫情数据下来清洗然后存储在MySQL中，实现了永久保存数据，以及实时更新数据，不仅方便，而且还能保证数据的安全性。

💡 [COVID-19-Django](https://gitee.com/Heng-Xiao/covid-19-django) 基于Django的国内疫情可视化平台，目前已开源分享。



* 🧑‍🤝‍🧑前端采用[Echarts](https://echarts.apache.org/zh/index.html) 、[Jquery](https://jquery.com/)、Ajax、HTML、CSS、。
* 💡后端采用 Python 语言 [Django](https://www.djangoproject.com/) 框架。



## 在线体验

👩‍👧‍👦演示地址：[http://www.henglulu.top](http://www.henglulu.top) 

- 账号：admin 

- 密码：admin




## 交流

-  covid-19-django交流群：812482043 [点击链接加入群聊](https://qm.qq.com/cgi-bin/qm/qr?k=aJVwjDvH-Es4MPJQuoO32N0SucK22TE5&jump_from=webapi)

- 二维码

  <img src='https://images.gitee.com/uploads/images/2022/0530/233203_5fb11883_5074988.jpeg' width='200'>

## 源码地址

gitee地址(主推)：[https://gitee.com/Heng-Xiao/covid-19-django](https://gitee.com/Heng-Xiao/covid-19-django)👩‍👦‍👦

github地址：[https://gitee.com/Heng-Xiao/covid-19-django](https://gitee.com/Heng-Xiao/covid-19-django)👩‍👦‍👦



## 内置功能

1.  👨‍⚕️用户登录：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。
2.  👩‍⚕️数据爬取：角色菜单权限分配、数据权限分配、设置角色按部门进行数据范围权限划分。
3.   :grapes: 数据更新：授权角色的权限范围。
4.  👨‍🎓疫情可视化大屏：用户是系统操作者，该功能主要完成系统用户配置。



## 准备工作
~~~
Python >= 3.8.0 (推荐3.8+版本)
Mysql >= 5.7.0 (可选，默认数据库sqlite3，推荐8.0版本)
PyCharm >= 2021
操作系统 (推荐Windows10版本)
~~~

## 运行准备♝

```bash
--安装依赖环境
pip install -r requirements.txt

--更换数据库密码
--进入connect.py和settings.py文件修改下

--connect.py
conn = Connect(user="root",
                   password="000000",
                   host="127.0.0.1",
                   database="covid-19",
                   port=3306,
                   charset="utf8", )
--settings.py
DATABASES = {
    'default':
    {
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎
        'NAME': 'covid-19', # 数据库名称
        'HOST': '127.0.0.1', # 数据库地址，本机 ip 地址 127.0.0.1
        'PORT': 3306, # 端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '000000', # 数据库密码
    }
}

--启动项目
python3 manage.py runserver 0.0.0.0:8000
```


### 访问项目

- 访问地址：[http://localhost:8000](http://localhost:8000) (默认为此地址，如有修改请按照配置文件)
- 账号：`admin` 密码：`admin`




## 演示图✅

![image-111](http://rt5c1mogb.hn-bkt.clouddn.com/1.png)

![image-01](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-01.jpg)

![image-02](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-02.jpg)

![image-03](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-03.jpg)

![image-04](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-04.jpg)

![image-05](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-05.jpg)

![image-06](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-06.jpg)

![image-07](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-07.jpg)

![image-08](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-08.jpg)

![image-09](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-09.jpg)

![image-10](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-10.jpg)

![image-11](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-11.jpg)

![image-12](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-12.jpg)

![image-13](https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/docs/demo-13.jpg)
