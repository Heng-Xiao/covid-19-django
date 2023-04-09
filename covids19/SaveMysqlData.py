#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author YangLuLu
# @date 2022/1/21
# @file SaveMysqlData.py
'''
专用于将爬取的疫情数据保存到MySql数据库
目前已经无用
'''
from covids19.GetData import *
from covids19.connect import get_engine
engine = get_engine()
def save_news():
    news = get_news()
    pd.io.sql.to_sql(news, 'news', con=engine, if_exists='append', index=None)
    print("最新新闻保存成功")
def save_news_value():
    news_value = get_news_value()
    pd.io.sql.to_sql(news_value, 'news_value', con=engine, if_exists='replace', index=None)
    print("最新新闻新闻数据统计分词保存成功")
def save_risk_areas():
    risk_areas = get_risk_areas()
    pd.io.sql.to_sql(risk_areas, 'risk_areas', con=engine, if_exists='replace', index=None)
    print("风险地区数据保存成功")
def save_china_total():
    china_total = get_china_total()
    pd.io.sql.to_sql(china_total, 'china_total', con=engine, if_exists='append', index=None)
    print("中国总数据保存成功")
def save_china_total_forqq():
    china_total_forqq = get_china_total_forqq()
    pd.io.sql.to_sql(china_total_forqq, 'china_total_forqq', con=engine, if_exists='append', index=None)
    print("腾讯疫情中国总数据保存成功")
def save_areaToday():
    areaTotal = get_areaTotal()
    pd.io.sql.to_sql(areaTotal, "area_today", con=engine, if_exists='replace', index=None)
    print("各省份总数据保存成功")
def save_area_history_confirm():
    area_history_confirm = get_area_history_confirm()
    pd.io.sql.to_sql(area_history_confirm, 'area_history_confirm', con=engine, if_exists='replace', index=None)
    print("各省份历史累计确诊数据保存成功")
def save_area_history_confirm_add():
    area_history_confirm_add = get_area_history_confirm_add()
    pd.io.sql.to_sql(area_history_confirm_add, 'area_history_confirm_add', con=engine, if_exists='replace', index=None)
    print("各省份历史现有确诊数据保存成功")
def save_chinaDayAdd():
    chinaDayAdd = get_chinaDayAdd()
    pd.io.sql.to_sql(chinaDayAdd, 'china_day_add', con=engine, if_exists='replace', index=None)
    print("中国每日增加历史数据保存成功")
def save_chinaDay():
    chinaDay = get_chinaDay()
    pd.io.sql.to_sql(chinaDay, 'china_day', con=engine, if_exists='replace', index=None)
    print("中国每日历史数据保存成功")
if __name__ == '__main__':
    save_area_history_confirm()#各省份历史累计确诊数据
    save_area_history_confirm_add()#各省份历史新增确诊数据
    save_news()#最新新闻表
    save_china_total()
    save_china_total_forqq()#中国总数据来自腾讯疫情网
    save_areaToday()#当日各省份总数据
    save_risk_areas()#风险地区数据
    save_chinaDayAdd()#中国每日新增历史数据
    save_chinaDay()#中国每日累计历史数据
    save_news_value()