import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

base_url = "https://glados.rocks/console/checkin"

option = webdriver.ChromeOptions()
option.add_argument('headless')  # 设置option
option.add_argument("headless")
option.add_argument('--no-sandbox')
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器


# driver.quit()
def getCookies():
    # 获取cookies保存到本地
    driver.get(base_url)
    # 预留一分钟时间登录邮箱，进入签到页面
    for i in range(60):
        time.sleep(1)
        print("\r{}".format(i), end='')
    print('')
    dict_cookies = driver.get_cookies()
    json_cookies = json.dumps(dict_cookies)  # 转换成字符串保存

    with open('glados_cookies.txt', 'w') as f:
        f.write(json_cookies)
    print('cookies保存成功！')


def checkin():
    # with open('glados_cookies.txt', 'r', encoding='utf8') as f:
    #     list_cookies = json.loads(f.read())
    list_cookies = json.loads(
        '[{"domain": ".glados.rocks", "expiry": 1712306461, "httpOnly": false, "name": "_ga_CZFVKMNT9J", "path": "/", "sameSite": "Lax", "secure": false, "value": "GS1.1.1677746396.1.1.1677746461.0.0.0"}, {"domain": ".glados.rocks", "expiry": 1712306453, "httpOnly": false, "name": "_ga", "path": "/", "sameSite": "Lax", "secure": false, "value": "GA1.1.627916546.1677746397"}, {"domain": "glados.rocks", "expiry": 1703666453, "httpOnly": true, "name": "koa:sess.sig", "path": "/", "sameSite": "Lax", "secure": false, "value": "NFhonEsYiEGXM1KlnPTjfP4ZXr0"}, {"domain": "glados.rocks", "expiry": 1703666453, "httpOnly": true, "name": "koa:sess", "path": "/", "sameSite": "Lax", "secure": false, "value": "eyJ1c2VySWQiOjE2NDQyNywiX2V4cGlyZSI6MTcwMzY2NjQyNjk0MSwiX21heEFnZSI6MjU5MjAwMDAwMDB9"}, {"domain": ".glados.rocks", "expiry": 1677832853, "httpOnly": false, "name": "_gid", "path": "/", "sameSite": "Lax", "secure": false, "value": "GA1.2.1878525009.1677746397"}]')
    driver.get(base_url)
    for cookie in list_cookies:
        cookie_dict = {
            'domain': '.glados.rocks',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'path': '/',
            "expires": '',
            'sameSite': 'None',
            'secure': cookie.get('secure')
        }
        driver.add_cookie(cookie_dict)

    # 更新cookies后进入目标网页
    driver.get(base_url)
    time.sleep(5)
    button = driver.find_element(By.TAG_NAME, "button")
    button.click()
    # print(button)
    time.sleep(5)
    return driver.find_element(By.XPATH, "//div[@class='row']/p").text + '\n' + driver.find_elements(By.CLASS_NAME, "content")[1].text


def pushMsg(content):
    token = '471ae9ed66004d57aecea9c82d7d1806'  # 改成你的token
    title = 'glados每日签到'
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)


if __name__ == "__main__":
    # getCookies()
    content = checkin()
    # print(content)
    pushMsg(content)
    driver.quit()
