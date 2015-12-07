#!/usr/bin/python

from flask import Flask
from flask import render_template
from investments import get_funded_loans
from agregate import summary
from operator import itemgetter
from flask.ext.cache import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/')
def index():
    return render_template("list_loans.html")


@app.route('/list_loans')
def listing():
    brt = cache.get('loans')
    if brt is None:
        listing = get_funded_loans()
        superlist = []
        # refactor this below
        for loan in listing:
            superlist.append([[loan], [summary(loan)['real_rate']]])
            supersorted = sorted(superlist, key=itemgetter(1))
            brt = supersorted[::-1]
        cache.set('loans', brt, timeout=6*60)
    return render_template("list_loans.html", superlist=brt)


if __name__ == '__main__':
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=5000)
