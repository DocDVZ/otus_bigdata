#! /usr/bin/env python
# -*- coding: utf-8 -*-
from KolchugaParser import KolchugaParser
import unicodecsv as csv



kp = KolchugaParser()
guns = kp.getAllGuns()
filename = "guns.csv"
# guns = kp.getPumpActionGuns()
with open(filename, mode='w') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "type","brand","name","country","price","caliber","description"])
    id = 1
    for gun in guns:
        writer.writerow([str(id), gun.type, gun.brand, gun.name, gun.country, gun.price, gun.caliber, gun.description])
        id+=1

