import requests
from operator import itemgetter
from matplotlib import pyplot as plt


def get_funded_loans():
    """
    Fetching current 100% loans available to bid
    """
    URL = "http://api.bitlendingclub.com/"
    QUERY = "api/loans?status=funding&denomination=btc&fundedFrom="
    FUNDED = 80
    raws = requests.get(URL+QUERY+str(FUNDED))
    loan_list = []
    for loan in raws.json()['loans']:
        loan_list.append(loan['id'])

    return loan_list


def summary(id):
    # Part to separate to make independent tests
    target = "https://api.bitlendingclub.com/api/investments/{id}"\
        .format(id=id)
    r = requests.get(target)
    totals = []
    inv = r.json()['investments']
    for i in range(0, len(r.json()['investments'])):
        totals.append([float(inv[i]['amount']), float(inv[i]['rate'])])
    # Sorting by rate value
    sbr = sorted(totals, key=itemgetter(1))
    total = 0  # total loan amount
    max_rate = 0  # Should be non zero if funded
    values = []
    rates = []
    raw = requests.get("https://api.bitlendingclub.com/api/loan/{id}"
                       .format(id=id))
    done = True
    # Caveat: Not 100% -> max rate could be same as current biggest
    for idx, part in enumerate(sbr):
        if total > float(raw.json()['loans'][0]['amount']) and done:
            max_rate = rates[-1]
            # print("Maximum rate {}".format(rates[-1]))
            done = False
        total = total + part[0]
        values.append(part[0])
        rates.append(part[1])
        last_inv = part[1]
    # Nominal rate and real rate etc

    info = {}
    keys = raw.json()['loans'][0].keys()
    term = raw.json()['loans'][0]['term']
    for key in keys:
        info[key] = raw.json()['loans'][0][key]
    # Max rate things
    if max_rate:
        real_rate = float(max_rate*(365.0/term))
    else:
        real_rate = float(last_inv*(365.0/term))
    info['real_rate'] = real_rate
    info['max_rate'] = max_rate
    return info


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

    plt.plot(values,rates)
    plt.ylabel('Nominal  %') #Ylabel
    plt.xlabel('Bitcoin amount')
    #Getting metadata about loan
    cutoff = float(raw.json()['loans'][0]['amount'])
    print("Loan amount: {}".format(cutoff))
    plt.axvline(cutoff, color='r', linewidth=10)
    #Different id
    filename = "static/images/{0}.png".format(id)
    plt.savefig(filename)
