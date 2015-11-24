from flask import Flask
from flask import render_template, url_for
from investments import loan_chart, get_funded_loans, weird
from agregate import *
from operator import itemgetter
import sys
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
cache = SimpleCache()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/list_loans')
def listing():
   brt = cache.get('loans')
   if brt is None:
      listing = get_funded_loans()
      superlist = []
      # TODO refactor this below
      for loan in listing:
        superlist.append( [ [loan], [ summary(loan)['real_rate'] ]] )
      supersorted = sorted(superlist, key=itemgetter(1))
      brt = supersorted[::-1]
      cache.set('loans', brt, timeout=5*60) 
   return render_template("list_loans.html", superlist=brt)


if __name__ == '__main__':
   app.config['DEBUG'] = False
   app.run(host='0.0.0.0', port=5000)
