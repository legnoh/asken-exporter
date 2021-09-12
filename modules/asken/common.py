from prometheus_client import CollectorRegistry, Gauge, write_to_textfile, Counter, Info

def login(driver, email, password):
    driver.get('https://www.asken.jp/login');
    driver.implicitly_wait(10);
    email_box = driver.find_element_by_name('data[CustomerMember][email]')
    email_box.send_keys(email)
    password_box = driver.find_element_by_name('data[CustomerMember][passwd_plain]')
    password_box.send_keys(password)
    email_box.submit()
    return driver
