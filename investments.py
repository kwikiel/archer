import requests
from operator import itemgetter


def get_funded_loans():
    """
    Fetching current 100% loans available to bid
    """

    raws = requests.get("http://api.bitlendingclub.com/api/loans?status=funding&denomination=btc&fundedFrom=10")
    loan_list = []
    for loan in raws.json()['loans']:
        loan_list.append(loan['id'])

    return loan_list


def best_rate(id):
    """
    Best nominal rate for investments
    """


    target = "https://api.bitlendingclub.com/api/investments/{id}".format(id=id)
    r = requests.get(target)
    totals = []
    inv = r.json()['investments']
    for i in range(0, len(r.json()['investments'])):
        totals.append([float(inv[i]['amount']), float(inv[i]['rate'])])
    #Sorting by rate value
    sbr = sorted(totals, key=itemgetter(1))
    return sbr[-1]

def weird(id):
    target = "https://api.bitlendingclub.com/api/investments/{id}".format(id=id)
    r = requests.get(target)

    totals = []
    inv = r.json()['investments']
    for i in range(0, len(r.json()['investments'])):
        totals.append(
                [float(inv[i]['amount']), float(inv[i]['rate'])]
                    )


    #Sorting by rate value
    sbr = sorted(totals, key=itemgetter(1))
    return sbr[-1]

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
    raw = requests.get("https://api.bitlendingclub.com/api/loan/{id}".format(id=id))
    done = True
    for idx,part in enumerate(sbr):
        if total>float(raw.json()['loans'][0]['amount']) and done:
            print("Maximum rate {}".format(rates[-1]))
            done=False
        total = total + part[0]
        values.append(total)
        rates.append(part[1])

    plt.plot(values,rates, linewidth=10.0)
    plt.ylabel('Nominal  %') #Ylabel
    plt.xlabel('Bitcoin amount')
    #Getting metadata about loan
    cutoff = float(raw.json()['loans'][0]['amount'])
    print("Loan amount: {}".format(cutoff))
    plt.axvline(cutoff, color='r', linewidth=10)
    #Different id
    filename = "static/images/{0}.png".format(id)
    plt.savefig(filename)
