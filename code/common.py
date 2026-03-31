import time  
import random  
import json
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta  
from playwright.sync_api import sync_playwright  

# 指定時區（例如 Asia/Taipei）
tz = ZoneInfo('Asia/Taipei')

# read config.json
with open("./config.json", "r") as jsonfile:
    configs = json.load(jsonfile)

def is_holiday(date):  
    return date.strftime("%Y-%m-%d") in configs['HOLIDAYS']

def is_weekend(date):  
    return date.weekday() >= 5  # 週六是5，週日是6  
  
def login_and_check_in(page):  
    page.fill('input[placeholder="公司代碼"]', configs['company_code'])  
    page.fill('input[placeholder="工號"]', configs['staff_id'])  
    page.fill('input[placeholder="請輸入您的密碼"]', configs['password'])  
    page.click('button:has-text("登入")')  
    page.wait_for_load_state('networkidle')  
  
def clock_in(page):  
    page.click('a[href="/ta?id=webpunch"]')  
    page.wait_for_load_state('networkidle')  
    page.click('button:has-text("上班")')  
    page.wait_for_timeout(5000)  # 5秒  
  
def clock_out(page):  
    page.click('a[href="/ta?id=webpunch"]')  
    page.wait_for_load_state('networkidle')  
    page.click('button:has-text("下班")')  
    page.wait_for_timeout(5000)  # 5秒  

def check_clock(date):
    # 取得當前時間並設定時區
    current_time = datetime.now(tz).time()

    # 定義時間範圍
    clock_in_start_time = datetime.strptime(configs['CLOCK_IN_TIME_START'], "%H:%M").time()
    clock_in_end_time = datetime.strptime(configs['CLOCK_IN_TIME_END'], "%H:%M").time()
    clock_out_start_time = datetime.strptime(configs['CLOCK_OUT_TIME_START'], "%H:%M").time()
    clock_out_end_time = datetime.strptime(configs['CLOCK_OUT_TIME_END'], "%H:%M").time()

    # 判斷目前時間是否在範圍內
    if clock_in_start_time <= current_time <= clock_in_end_time:
        return 1 # good time for clock in
    elif clock_out_start_time <= current_time <= clock_out_end_time:
        return -1 # good time for clock out
    else:
        return 0 # no good for clock in/out

