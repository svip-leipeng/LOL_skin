import os
import time
import random
from bs4 import BeautifulSoup
import requests

# 假设你有一个代理IP列表（实际应用中需要替换为真实有效的代理）
proxy_list = [
    {"http": "http://ip1:port"},
    {"http": "http://ip2:port"},
    # 更多代理...
]

def get_hero_list():
    url = "https://lol.qq.com/web201311/info-heros.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    hero_list = []
    for li in soup.find_all("li", class_="heroul_li"):
        hero_name = li.find("a").text
        hero_list.append(hero_name)
    return hero_list

def get_hero_skins(hero_name):
    proxy = random.choice(proxy_list)
    proxies = {"http": proxy["http"], "https": proxy["https"]} if proxy else None

    url = f"https://lol.qq.com/web201311/info-heros-detail/{hero_name}.shtml"
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    skin_list = []
    for div in soup.find_all("div", class_="skin_item"):
        skin_name = div.find("img")["alt"]
        skin_list.append(skin_name)
    return skin_list

def download_skin(skin_name, save_path):
    proxy = random.choice(proxy_list)
    proxies = {"http": proxy["http"], "https": proxy["https"]} if proxy else None

    url = f"https://ossweb-img.qq.com/images/lol/web201311/skin/big{skin_name}.jpg"
    response = requests.get(url, proxies=proxies)
    with open(os.path.join(save_path, f"{skin_name}.jpg"), "wb") as f:
        f.write(response.content)

# ... 其他部分代码不变 ...

if __name__ == "__main__":
    main()
