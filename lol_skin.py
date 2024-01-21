import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# 假设你有一个代理IP列表（实际应用中需要替换为真实有效的代理）
proxy_list = [
    {"http": "http://ip1:port"},
    {"http": "http://ip2:port"},
    # 更多代理...
]


def check_proxy(proxy):
    """
    检查代理是否有效
    """
    try:
        response = requests.get("http://www.baidu.com", proxies=proxy, timeout=5)
        return response.status_code == 200
    except:
        return False


def get_proxies():
    """
    获取可用的代理
    """
    proxies = []
    for proxy in proxy_list:
        if check_proxy(proxy):
            proxies.append(proxy)
    return random.choice(proxies) if proxies else None


def request_with_proxy(url, proxies=None):
    """
    使用代理发送请求
    """
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()  # 触发HTTPError来处理错误状态
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_hero_list():
    url = "https://lol.qq.com/web201311/info-heros.shtml"
    soup = BeautifulSoup(request_with_proxy(url).text, "html.parser")
    hero_list = [li.find("a").text for li in soup.find_all("li", class_="heroul_li")]
    return hero_list


def get_hero_skins(hero_name):
    proxies = get_proxies()
    url = f"https://lol.qq.com/web201311/info-heros-detail/{quote(hero_name)}.shtml"
    soup = BeautifulSoup(request_with_proxy(url, proxies).text, "html.parser")
    skin_list = [div.find("img")["alt"] for div in soup.find_all("div", class_="skin_item")]
    return skin_list


def download_skin(skin_name, save_path):
    proxies = get_proxies()
    url = f"https://ossweb-img.qq.com/images/lol/web201311/skin/big{skin_name}.jpg"
    response = request_with_proxy(url, proxies)

    if response and response.content:
        skin_file_path = os.path.join(save_path, f"{skin_name}.jpg")
        os.makedirs(save_path, exist_ok=True)
        with open(skin_file_path, "wb") as f:
            f.write(response.content)
            print(f"Skin {skin_name} downloaded successfully.")


# ... 其他部分代码不变 ...

if __name__ == "__main__":
    main()