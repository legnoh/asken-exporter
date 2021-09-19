import datetime
from selenium.common.exceptions import NoSuchElementException

def login(driver, email, password):
    driver.get('https://www.asken.jp/login')
    driver.implicitly_wait(10)
    email_box = driver.find_element_by_name('data[CustomerMember][email]')
    email_box.send_keys(email)
    password_box = driver.find_element_by_name('data[CustomerMember][passwd_plain]')
    password_box.send_keys(password)
    email_box.submit()
    return driver

def is_premium(driver):
    driver.get('https://www.asken.jp/setting/premium')
    try:
        menu_name = driver.find_element_by_css_selector("div#setting_premium > div.left > div.gbox_top").text
        if menu_name == "プレミアムサービス解約手続き":
            return True
    except NoSuchElementException:
        return False
    return False

def get_latest_daily_score(driver):
    score = None
    target_date = datetime.datetime.now()
    format_date = target_date.strftime('%Y-%m-%d')

    while score == None:
        driver.get('https://www.asken.jp/wsp/advice/'+ format_date +'/0');
        try:
            score = int(driver.find_element_by_css_selector("div#fuki > p > span.stressed_advice > span.ft_red").text.rstrip("点"))
            return score
        except NoSuchElementException:
            target_date = target_date - datetime.timedelta(days=1)
            format_date = target_date.strftime('%Y-%m-%d')

def get_advice(driver, path, premium=False):
    target_date = datetime.datetime.now()
    format_date = target_date.strftime('%Y-%m-%d')
    advice = None
    i = 0
    while advice == None or i > 30:
        driver.get('https://www.asken.jp/wsp/advice/'+ format_date + path);
        try:
            if path == '/0' and premium:
                try:
                    advice = driver.find_element_by_css_selector("div#premium_fuki_comment").text
                except NoSuchElementException:
                    advice = driver.find_element_by_css_selector("div#fuki > p").text
            else:
                advice = driver.find_element_by_css_selector("div#fuki > p").text
            return advice
        except NoSuchElementException:
            target_date = target_date - datetime.timedelta(days=1)
            format_date = target_date.strftime('%Y-%m-%d')
            i += 1
    return "食事記録が無いためアドバイスが取得できません。"

def get_detail_advice(driver):
    try:
        advice = driver.find_element_by_css_selector("div#detail_advice > div.text_advice").text
        return advice
    except NoSuchElementException:
        return "食事記録が無いためアドバイスが計算できません。"
