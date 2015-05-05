import requests
from operator import itemgetter
from matplotlib import pyplot as plt

def loan_chart(id):
    target = "https://api.bitlendingclub.com/api/investments/{id}".format(id=id)
    r = requests.get(target)

    totals = []
    inv = r.json()['investments']
    for i in range(0, len(r.json()['investments'])):
        totals.append(
                [float(inv[i]['amount']), float(inv[i]['rate'])]
                    )
        print("Amount: {0}, rate: {1}".format(inv[i]['amount'], inv[i]['rate']))


    #Sorting by rate value
    sbr = sorted(totals, key=itemgetter(1))
    total = 0 # total loan amount
    values = []
    rates = []
    for part in sbr:
        total = total + part[0]
        values.append(total)
        rates.append(part[1])

    plt.plot(values,rates)
    plt.ylabel('Nominal  %') #Ylabel
    plt.xlabel('Bitcoin amount')
    plt.axvline(x=1.2, color='r')
    #Different id
    filename = "/home/kacper/lendon/static/images/{0}.png".format(id)
    plt.savefig(filename)

