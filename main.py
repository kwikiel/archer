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

@app.route('/nice/<int:id>')
def nice_view(id):
   info = summary(id)
   id = id
   loan_chart(id)
   return render_template("nice.html", info=info, id=id)


@app.route('/list_loans')
def listing():
   brt = cache.get('loans')
   if brt is None:
      listing = get_funded_loans()
      superlist = []
      for loan in listing:
        superlist.append( [ [loan], [ summary(loan)['real_rate'] ]] )
      supersorted = sorted(superlist, key=itemgetter(1))
      brt = supersorted[::-1]
      cache.set('loans', brt, timeout=5*60) 
   return render_template("list_loans.html", superlist=brt)


@app.route('/loan/<int:id>')
def charts(id):
   loan_chart(id)
   all_data = summary(id)
   return render_template("loan.html", id=id, all_data = all_data)

if __name__ == '__main__':
   app.config['DEBUG'] = False
   app.run(host='0.0.0.0', port=5000)
