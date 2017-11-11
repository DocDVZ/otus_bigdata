

class Gun:

    SMOOTH_SEMI_AUTO = "smooth-semi-auto"
    SMOOTH_DUAL_BARREL_H = "horizontal dual-barrel"
    SMOOTH_DUAL_BARREL_V = "vertical dual-barrel"
    SMOOTH_PUMP_ACTION = "pump-action"
    RIFLED_SEMI_AUTO = "rifled-semi-auto"
    RIFLED_BOLT_ACTION = "bolt-action"
    RIFLED_COMBI = "combi"



    def __init__(self, name):
        self.name = name
        self.url = None
        self.price = None
        self.type = None
        self.brand = None
        self.country = None
        self.caliber = None
        self.country = None
        self.description = None


    def setUrl(self, url):
        self.url = url

    def setPrice(self, price):
        self.price = price

    def setType(self, type):
        self.type = type

    def setBrand(self, brand):
        self.brand = brand

    def setCountry(self, country):
        self.country = country

    def setCaliber(self, caliber):
        self.caliber = caliber

    def setDescr(self, description):
        self.description = description
