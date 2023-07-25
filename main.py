import os, platform, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.service import Service as ChromeService

import modules.asken as asken
from prometheus_client import CollectorRegistry, Gauge, Info, start_http_server

if __name__ == '__main__':

    # initialize exporter
    print("initializing exporter...")
    registry = CollectorRegistry()
    start_http_server(int(os.environ.get('PORT', 8000)), registry=registry)

    # initialize chromium & selenium webdriver
    print("initializing chromium & selenium webdriver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')

    if platform.system() == 'Linux':
        driver = webdriver.Chrome(service=ChromiumService(), options=options)
    else:
        driver = webdriver.Chrome(service=ChromeService(), options=options)

    today = time.strftime("%Y-%m-%d")

    # login
    print("login to asken...")
    username = os.environ['ASKEN_USERNAME']
    password = os.environ['ASKEN_PASSWORD']
    ak_driver = asken.login(driver, username, password)

    metrics = {
        "daily": {},
        "weekly": {},
        "monthly": {},
    }

    advice_targets = [
        { 'name': 'daily', 'path': '/0', 'desc': '1日分' },
        { 'name': 'weekly', 'path': '/1', 'desc': '過去7日の平均' },
        { 'name': 'monthly', 'path': '/2', 'desc': '月平均' },
    ]

    # premium?
    premium = asken.is_premium(driver)

    # create metrics
    print("create metrics instances...")
    score_gauge = Gauge("asken_score", "あすけん > 健康度", registry=registry)
    for target in advice_targets:
        metrics[target['name']]['advice'] = Info(
            "asken_{n}_advice".format(n=target['name']),
            "あすけん > アドバイス > {d}".format(d=target['desc']),
            registry=registry
        )
        metrics[target['name']]['detail_advice'] = Info(
            "asken_{n}_detail_advice".format(n=target['name']),
            "あすけん > 栄養価アドバイス > {d}".format(d=target['desc']),
            registry=registry
        )

    while True:

        # get daily score
        print("getting daily score...")
        daily_score = asken.get_latest_daily_score(ak_driver)
        score_gauge.set(daily_score)

        # get advice
        print("getting advices...")
        for target in advice_targets:
            advice = asken.get_advice(ak_driver, target['path'], premium)
            metrics[target['name']]['advice'].info( { "advice": advice } )

            detail_advice = asken.get_detail_advice(ak_driver)
            metrics[target['name']]['detail_advice'].info( { "advice": detail_advice } )

        print("scraping account is successfully.")

        ak_driver.close()

        time.sleep(3600*4)
