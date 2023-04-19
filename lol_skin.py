# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2/25/2020 2:24 PM
# @Author   : XiaoXia
# @Blog     : https://xiaoxiablogs.top
# @File     : lol_hero_photo.py
import datetime

import requests
import simplejson
import os
import threading


# 多线程版本
class HeroImage(threading.Thread):
    # lol英雄获取英雄皮肤列表网站
    url_demo = "https://game.gtimg.cn/images/lol/act/img/js/hero/"
    # 设置ua
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
    headers = {
        'User-Agent': ua
    }

    def __init__(self, hero_id, hero_name):
        threading.Thread.__init__(self)
        self.hero_id = hero_id
        self.hero_name = hero_name.replace("/", "")

    def run(self):
        print("{}的皮肤爬取开始了!!!".format(self.hero_name))
        hero_images_list = self.getImagesUrl()
        self.dirIsExist()
        for hero_images in hero_images_list:
            self.saveImage(hero_images["url"], hero_images['name'].replace("/", ""))
        print("{}皮肤爬取完成!!!".format(self.hero_name))

    def dirIsExist(self):
        """
        判断文件夹是否存在,不存在则创建
        """
        if not os.path.exists("./hero/"):
            os.mkdir("./hero/")
        path = "./hero/{}/".format(self.hero_name)
        if not os.path.exists(path):
            os.mkdir(path)

    def getImagesUrl(self) -> list:
        """
        获取皮肤照片链接
        :return: 皮肤照片数组
        """
        response = self.getJson(self.url_demo + self.hero_id + ".js")
        images = simplejson.loads(response.text)['skins']
        image_list = []
        '''
        skinId: 图片的编号
        name: 皮肤名称
        mainImg: 图片地址
        '''
        for image in images:
            image_dic = {
                "name": image['name'],
                "url": image['mainImg']
            }
            # 由于其中还有一些炫彩模型，所以要去除掉
            if image_dic['url']:
                image_list.append(image_dic)

        return image_list

    def saveImage(self, url: str, image_name: str):
        """
        通过链接获取图片并且将图片保存到相应的目录下
        :param path: 保存目录
        :param image_name: 图片名称
        :param url: 图片地址
        """
        response = requests.get(url, headers=self.headers)
        image_path = "./hero/{}/{}.jpg".format(self.hero_name, image_name)

        with response:
            # 得到图片的二进制文件
            image_file = response.content
            with open(image_path, "wb+") as f:
                f.write(image_file)
                f.flush()

    @staticmethod
    def getJson(hero_url: str) -> requests.models.Response:
        """
            获取json响应
            :param hero_url: 英雄列表的获取链接
            :return:
            """
        response = requests.get(hero_url, headers=HeroImage.headers)
        return response


if __name__ == "__main__":
    # 用于计算程序运行时间的，不需要可直接删除该语句
    start_time = datetime.datetime.now()
    # lol英雄列表
    hero_list = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    jsons = HeroImage.getJson(hero_list)
    heros = simplejson.loads(jsons.text)["hero"]
    for hero in heros:
        '''
        编号: heroId
        称号: name
        英文名: alias
        中文名: title
        '''
        name = hero['name'] + '-' + hero['title']

        name = name.replace("/", "")
        thread = HeroImage(hero['heroId'], name)
        thread.start()
        print(threading.active_count())
    # 用于计算程序运行时间的，不需要可直接删除该循环
    while True:
        if threading.active_count() <= 1:
            print("全部爬取完毕")
            end_time = datetime.datetime.now()
            print("总用时为:", end_time-start_time)
            break

