#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
from lxml import etree
from Items import Gun
import re


class KolchugaParser:
    __rootUrl = "https://www.kolchuga.ru"
    __smoothBarrelUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/gladkostvolnoe-oruzhie/"
    __semiAutoUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/gladkostvolnoe-oruzhie/samozaryadnoe_1/"
    __duoBarrelVUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/gladkostvolnoe-oruzhie/dvustvolnoe-vertikalnoe/"
    __duoBarrelHUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/gladkostvolnoe-oruzhie/dvustvolnoe-gorizontalnoe/"
    __pumpActionUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/gladkostvolnoe-oruzhie/pompovoe/"
    __rifledSemiAutoUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/nareznoe-oruzhie/samozaryadnoe/"
    __rifledBoltActionUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/nareznoe-oruzhie/s-prodolno-skolzyashchim-zatvorom/"
    __rifledCombiUrl = "https://www.kolchuga.ru/internet_shop/oruzhie/nareznoe-oruzhie/kombinirovannoe/"
    __pageSuffix = "?PAGEN_1="


    def getAllGuns(self):
        guns = []
        guns += self.getSmoothSemiAutoGuns()
        print "Processed semi-auto shotguns, guns added: " + str(len(guns))
        guns += self.getDualBArreledVerticalGuns()
        print "Processed vertical dual-barreled shotguns, guns added: " + str(len(guns))
        guns += self.getDualBarrelHorizontalGuns()
        print "Processed horizontal dual-barreled shotguns, guns added: " + str(len(guns))
        guns += self.getPumpActionGuns()
        print "Processed pump-action shotguns, guns added: " + str(len(guns))
        guns += self.getRifledSemiAutoGuns()
        print "Processed semi-auto rifles, guns added: " + str(len(guns))
        guns += self.getRifledBoltActionGuns()
        print "Processed bolt rifles, guns added: " + str(len(guns))
        guns += self.getRifledCombiGuns()
        print "Processed combi rifles, guns added: " + str(len(guns))
        return guns


    def getSmoothSemiAutoGuns(self):
        page  = requests.get(self.__semiAutoUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__semiAutoUrl, maxPage, Gun.SMOOTH_SEMI_AUTO)


    def getDualBArreledVerticalGuns(self):
        page = requests.get(self.__duoBarrelVUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__duoBarrelVUrl, maxPage, Gun.SMOOTH_DUAL_BARREL_V)


    def getDualBarrelHorizontalGuns(self):
        page = requests.get(self.__duoBarrelHUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__duoBarrelHUrl, maxPage, Gun.SMOOTH_DUAL_BARREL_H)


    def getPumpActionGuns(self):
        page = requests.get(self.__pumpActionUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__pumpActionUrl, maxPage, Gun.SMOOTH_PUMP_ACTION)


    def getRifledSemiAutoGuns(self):
        page = requests.get(self.__rifledSemiAutoUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__rifledSemiAutoUrl, maxPage, Gun.RIFLED_SEMI_AUTO)


    def getRifledBoltActionGuns(self):
        page = requests.get(self.__rifledBoltActionUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__rifledBoltActionUrl, maxPage, Gun.RIFLED_BOLT_ACTION)


    def getRifledCombiGuns(self):
        page = requests.get(self.__rifledCombiUrl).text
        maxPage = self.__getMaxPage(page)
        return self.__getGuns(self.__rifledCombiUrl, maxPage, Gun.RIFLED_COMBI)


    def __getMaxPage(self, page):
        arr = html.fromstring(page).xpath('//ul[@class="pagination"]/li')
        if len(arr) >2:
            return int(arr[-2].xpath('.//a/span')[0].text) + 1
        else:
            return 2



    def __getGuns(self, root_url, maxPage, gunType):
        guns = []
        for i in xrange(1, maxPage):
            pageUrl = root_url + self.__pageSuffix + str(i)
            req = requests.get(pageUrl)
            page = req.text
            tree = html.fromstring(page)
            divs = tree.xpath('//div[@class="catalog__item"]')
            for elem in divs:
                # print dir(elem)
                title = elem.xpath('.//div[@class="catalog__item-title"]/a')[0].text.encode('utf-8').replace("\"", "")
                gunUrl = elem.xpath('.//div[@class="catalog__item-title"]/a/@href')[0].encode('utf-8')
                priceText = elem.xpath('.//div[@class="catalog__item-price"]/span')[0].text.encode('utf-8')
                match = re.search("([0-9 ]+)((?=( [a-zA-Zа-яА-Я]+))|($))", priceText)
                if match:
                    price = int(match.group().replace(" ", ""))
                gun = Gun(title)
                gun.setPrice(price)
                gun.setType(gunType)
                gun.setUrl(self.__rootUrl + gunUrl)
                gunReq = requests.get(gun.url)
                gunTree = html.fromstring(gunReq.text)
                descr = gunTree.xpath('.//div[@class="catalog__param"]/div[@class="catalog__param--left"]/ul')
                properties = dict()
                for elem in descr:
                    for li in elem.iterdescendants():
                        text = etree.tostring(li, encoding="utf-8")
                        keyMatcher = re.search("(?<=<em>).+(?=<\/em>)", text)
                        key = None
                        if keyMatcher:
                            key = keyMatcher.group()
                        valueMatcher = re.search("(?<=<b>).+(?=<\/b>)", text)
                        if valueMatcher:
                            value = valueMatcher.group()
                        if key:
                            properties[key] = value
                # detailDesc = etree.tostring(gunTree.xpath('//div[@class="catalog__detail--desc"]')[0], encoding="utf-8")
                # detailDesc = re.sub("(<[^<>]*>)|(\")|(&#.*;)", "", detailDesc).replace("\n", " || ")
                gun.setBrand(properties.get("Бренд"))
                gun.setCountry(properties.get("Страна"))
                gun.setCaliber(properties.get("Калибр"))
                # gun.setDescr(detailDesc)
                guns.append(gun)
        return guns
