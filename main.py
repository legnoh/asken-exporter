import os
import time
from selenium import webdriver
import chromedriver_binary
import modules.asken as asken
from prometheus_client import CollectorRegistry, Gauge, Info, write_to_textfile

# initialize
registry = CollectorRegistry()
driver = webdriver.Chrome()

today = time.strftime("%Y-%m-%d")

# login
username = os.environ['ASKEN_USERNAME']
password = os.environ['ASKEN_PASSWORD']
ak_driver = asken.login(driver, username, password)

# premium?
premium = asken.is_premium(driver)

# get daily score
daily_score = asken.get_latest_daily_score(ak_driver)
score_gauge = Gauge("asken_score", "あすけん > 健康度", registry=registry)
score_gauge.set(daily_score)

metrics = {}
targets = [
    { 'name': 'daily', 'path': '/0', 'desc': '1日分' },
    { 'name': 'weekly', 'path': '/1', 'desc': '過去7日の平均' },
    { 'name': 'monthly', 'path': '/2', 'desc': '月平均' },
]

for target in targets:
    advice = asken.get_advice(driver, target['path'], premium)
    detail_advice = asken.get_detail_advice(driver)
    advice_info = Info("asken_" + target['name'] + "_advice", "あすけん > アドバイス > " + target['desc'], registry=registry)
    advice_info.info( { "advice": advice } )
    detail_advice_info = Info("asken_" + target['name'] + "_detail_advice", "あすけん > 栄養価アドバイス > " + target['desc'], registry=registry)
    detail_advice_info.info( { "advice": detail_advice } )

ak_driver.quit()
write_to_textfile('./container/public/asken.prom', registry)
print("scraping account is successfull!")
