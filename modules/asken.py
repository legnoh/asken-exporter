import base64, datetime, logging, os, time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def login(driver:WebDriver, email:str, password:str) -> WebDriver | None:
    try:
        logging.info("## jump to login page...")
        driver.get('https://www.asken.jp/login')

        email_box = driver.find_element(By.NAME, 'data[CustomerMember][email]')
        email_box.send_keys(email)
        password_box = driver.find_element(By.NAME, 'data[CustomerMember][passwd_plain]')
        password_box.send_keys(password)
        email_box.submit()

        # ログイン実行後もまだloginがURLに含まれる場合、ログインに失敗していると判定する
        if  '/login' in driver.current_url:
            logging.error("## login check was failed. plase check your email & password!")
            return None

        logging.info("## login check successfully")
        return driver

    except NoSuchElementException as e:
        logging.error("## login failed with selenium error: %s", e.msg)
        save_debug_information(driver, "login")
        return None

def is_premium(driver:WebDriver) -> bool:
    driver.get('https://www.asken.jp/setting/premium')
    try:
        menu_name = driver.find_element(By.CSS_SELECTOR, "div#setting_premium > div.left > div.gbox_top").text
        if menu_name == "プレミアムサービス解約手続き":
            return True
    except NoSuchElementException:
        return False
    return False

def get_latest_daily_score(driver:WebDriver) -> int:
    score = None
    target_date = datetime.datetime.now()
    format_date = target_date.strftime('%Y-%m-%d')

    while score == None:
        driver.get('https://www.asken.jp/wsp/advice/'+ format_date +'/0');
        try:
            score = int(driver.find_element(By.CSS_SELECTOR, "div#fuki > p > span.stressed_advice > span.ft_red").text.rstrip("点"))
            return score
        except NoSuchElementException:
            target_date = target_date - datetime.timedelta(days=1)
            format_date = target_date.strftime('%Y-%m-%d')

def get_advice(driver:WebDriver, path:str, premium=False) -> str:
    target_date = datetime.datetime.now()
    format_date = target_date.strftime('%Y-%m-%d')
    advice = None
    i = 0
    while advice == None or i > 30:
        driver.get('https://www.asken.jp/wsp/advice/'+ format_date + path);
        try:
            if path == '/0' and premium:
                try:
                    advice = driver.find_element(By.CSS_SELECTOR, "div#premium_fuki_comment").text
                except NoSuchElementException:
                    advice = driver.find_element(By.CSS_SELECTOR, "div#fuki > p").text
            else:
                advice = driver.find_element(By.CSS_SELECTOR, "div#fuki > p").text
            return advice
        except NoSuchElementException:
            target_date = target_date - datetime.timedelta(days=1)
            format_date = target_date.strftime('%Y-%m-%d')
            i += 1
    return "食事記録が無いためアドバイスが取得できません。"

def get_detail_advice(driver:WebDriver) -> str:

    try:
        advice = driver.find_element(By.CSS_SELECTOR, "div#detail_advice > div.text_advice").text
        return advice
    except NoSuchElementException:
        return "食事記録が無いためアドバイスが計算できません。"

def save_debug_information(driver:WebDriver, error_slug: str) -> None:

    issuetitle = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + error_slug
    debugfile_dir = os.getenv("DEBUGFILE_DIR", "/tmp/asken-exporter")

    if not os.path.exists(debugfile_dir):
        os.makedirs(debugfile_dir)

    # save sourcecode
    sourcecode = driver.execute_script("return document.body.innerHTML;")
    sourcecode_path = debugfile_dir + "/" + issuetitle + ".html"
    with open(sourcecode_path, "w") as f:
        f.write(sourcecode)
    logging.info("### sourcecode: %s", sourcecode_path)

    # save screenshot
    screenshot_data = base64.urlsafe_b64decode(driver.execute_cdp_cmd("Page.captureScreenshot", {"captureBeyondViewport": True})["data"])
    screenshot_path = debugfile_dir + "/" + issuetitle + ".png"
    with open(screenshot_path, "wb") as f:
        f.write(screenshot_data)
    logging.info("### screenshot: %s", screenshot_path)
