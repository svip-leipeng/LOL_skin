import os
import time
import random
from bs4 import BeautifulSoup
import requests

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
    url = f"https://lol.qq.com/web201311/info-heros-detail/{hero_name}.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    skin_list = []
    for div in soup.find_all("div", class_="skin_item"):
        skin_name = div.find("img")["alt"]
        skin_list.append(skin_name)
    return skin_list

def download_skin(skin_name, save_path):
    url = f"https://ossweb-img.qq.com/images/lol/web201311/skin/big{skin_name}.jpg"
    response = requests.get(url)
    with open(os.path.join(save_path, f"{skin_name}.jpg"), "wb") as f:
        f.write(response.content)

def main():
    hero_list = get_hero_list()
    print("请选择要下载的英雄：")
    for i, hero_name in enumerate(hero_list):
        print(f"{i + 1}. {hero_name}")
    selected_heroes = input("请输入英雄编号，用逗号分隔：").split(",")
    selected_heroes = [int(x) - 1 for x in selected_heroes]

    save_path = input("请输入保存皮肤的文件夹路径：")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for hero_index in selected_heroes:
        hero_name = hero_list[hero_index]
        print(f"正在下载 {hero_name} 的皮肤...")
        skin_list = get_hero_skins(hero_name)
        for skin_name in skin_list:
            print(f"正在下载 {skin_name} ...")
            download_skin(skin_name, save_path)
            time.sleep(random.randint(1, 10))
        print(f"{hero_name} 的皮肤下载完成！")
        time.sleep(random.randint(1, 10))

if __name__ == "__main__":
    main()
