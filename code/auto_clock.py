import time  
import random  
from datetime import datetime, timedelta  
from playwright.sync_api import sync_playwright  
from common import is_weekend, is_holiday, login_and_check_in, clock_in, check_clock

def run(playwright):  
    now = datetime.now()  

    if is_weekend(now) or is_holiday(now):  
        print("今天是週末或國定假日，不打卡")  
        return  

    if check_clock(now) == 0:
        print("不在打卡時間內，不打卡")  
        return  

    browser = playwright.chromium.launch(headless=True)  
    page = browser.new_page()  
    page.goto("https://asiaauth.mayohr.com/HRM/Account/Login?original_target=https://apollo.mayohr.com/tube&lang=zh-tw&utm_source=google&utm_medium=cpc&utm_campaign=pmax%E6%89%93%E5%8D%A1%E7%B3%BB%E7%B5%B1%EF%BC%86utm_content=&utm_term=&gad_source=1&gclid=CjwKCAiAm-67BhBlEiwAEVftNmHCa7tTiFiOgcLJKk63cGj1O7vNZgwFzLMzSlaHGv720kuZrEEpMRoCuKoQAvD_BwE")  
    login_and_check_in(page)  
  
    if check_clock(now) == 1:
        try:  
            clock_in(page)  
            print("上班打卡成功")  
        except Exception as e:  
            print(f"上班打卡失敗: {e}")  
        finally:  
            browser.close()  
    elif check_clock(now) == -1:
        try:  
            clock_out(page)  
            print("下班打卡成功")  
        except Exception as e:  
            print(f"下班打卡失敗: {e}")  
        finally:  
            browser.close()  
  
with sync_playwright() as playwright:  
    run(playwright)  
