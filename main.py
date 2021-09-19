import os
import time
from selenium import webdriver
import chromedriver_binary
import modules.asken.common as asken
from prometheus_client import CollectorRegistry, Gauge, Info, write_to_textfile

# initialize
registry = CollectorRegistry()
driver = webdriver.Chrome()

today = time.strftime("%Y-%m-%d")

# login
username = os.environ['ASKEN_USERNAME']
password = os.environ['ASKEN_PASSWORD']
ak_driver = asken.login(driver, username, password)

# get today score and advice
driver.get('https://www.asken.jp/wsp/advice/'+ today +'/0');
try:
    int(today_score = driver.find_element_by_css_selector("div#fuki > p > span.stressed_advice > span.ft_red").text.rstrip("点"))
except:
    today_score = 0
try:
    today_advice = driver.find_element_by_css_selector("div#fuki > p").text
    today_detail_advice = driver.find_element_by_css_selector("div#detail_advice > div.text_advice").text
except:
    today_advice = "食事記録が無いためアドバイスが計算できません。"
    today_detail_advice = "食事記録が無いためアドバイスが計算できません。"

score_gauge = Gauge("asken_today_score", "Asken Today's score", ['date'], registry=registry)
advice_info = Info("asken_today_advice", "Asken Today's advice", ['date'], registry=registry)
detail_advice_info = Info("asken_today_detail_advice", "Asken Today's detail advice", ['date'], registry=registry)
score_gauge.labels(today).set(today_score)
advice_info.labels(today).info( { "advice": today_advice } )
detail_advice_info.labels(today).info( { "advice": today_detail_advice } )

# get weekly advice
driver.get('https://www.asken.jp/wsp/advice/'+ today +'/1');
try:
    weekly_advice = driver.find_element_by_css_selector("div#fuki > p").text
    weekly_detail_advice = driver.find_element_by_css_selector("div#detail_advice > div.text_advice").text
except:
    weekly_advice = "食事記録が無いためアドバイスが計算できません。"
    weekly_detail_advice = "食事記録が無いためアドバイスが計算できません。"

weekly_advice_info = Info("asken_weekly_advice", "Asken weekly advice", ['date'], registry=registry)
weekly_detail_advice_info = Info("asken_weekly_detail_advice", "Asken weekly detail advice", ['date'], registry=registry)
weekly_advice_info.labels(today).info( { "advice": weekly_advice } )
weekly_detail_advice_info.labels(today).info( { "advice": weekly_detail_advice } )

# get monthly advice
driver.get('https://www.asken.jp/wsp/advice/'+ today +'/2');
try:
    monthly_advice = driver.find_element_by_css_selector("div#fuki > p").text
    monthly_detail_advice = driver.find_element_by_css_selector("div#detail_advice > div.text_advice").text
except:
    monthly_advice = "食事記録が無いためアドバイスが計算できません。"
    monthly_detail_advice = "食事記録が無いためアドバイスが計算できません。"

monthly_advice_info = Info("asken_monthly_advice", "Asken monthly advice", ['date'], registry=registry)
monthly_detail_advice_info = Info("asken_monthly_detail_advice", "Asken monthly detail advice", ['date'], registry=registry)
monthly_advice_info.labels(today).info( { "advice": monthly_advice } )
monthly_detail_advice_info.labels(today).info( { "advice": monthly_detail_advice } )

ak_driver.quit()
write_to_textfile('./container/public/asken.prom', registry)
print("scraping account is successfull!")
