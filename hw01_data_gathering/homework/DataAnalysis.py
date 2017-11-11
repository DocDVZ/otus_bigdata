import matplotlib.pyplot as plt
import csv
import pandas as pd
from pandas.plotting import scatter_matrix
from Items import Gun



def stats():
    guns = getGunsFromCsv()
    prices = map(lambda x: x.price, guns)
    # DataFrame
    df = pd.DataFrame({
        "type": map(lambda x: x.type, guns),
        "brand": map(lambda x: x.brand, guns),
        "country": map(lambda x: x.country, guns),
        "name": map(lambda x: x.name, guns),
        "caliber": map(lambda x: x.country, guns),
        "price": map(lambda x: x.price, guns),
    })
    print df.head()
    print df.info()
    print df.describe()
    print df['country'].value_counts()
    print df['brand'].value_counts()
    print df['type'].value_counts()
    # Price hist
    plt.hist([price for price in prices], bins=100)
    plt.show()


def getGunsFromCsv():
    guns = []
    with open('guns.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        isFirst = True
        for row in reader:
            if isFirst:
                isFirst = False
                continue
            gun = Gun(unicode(row[3], 'utf-8'))
            gun.setType(unicode(row[1], 'utf-8'))
            gun.setCountry(unicode(row[4], 'utf-8'))
            gun.setBrand(unicode(row[2], 'utf-8'))
            gun.setPrice(int(unicode(row[5].encode('utf-8'))))
            gun.setCaliber(unicode(row[6], 'utf-8'))
            guns.append(gun)
    return guns


