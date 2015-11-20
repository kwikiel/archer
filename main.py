from flask import Flask
from flask import render_template, url_for
from investments import loan_chart, get_funded_loans, weird
from agregate import *
from operator import itemgetter
app = Flask(__name__)

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
   listing = get_funded_loans()
   superlist = []
   for loan in listing:
      superlist.append( [ [loan], [ summary(loan)['real_rate'] ]] )
   supersorted = sorted(superlist, key=itemgetter(1))
   brt = supersorted[::-1]
   return render_template("list_loans.html", listing=listing, superlist=brt)


@app.route('/loan/<int:id>')
def charts(id):
   loan_chart(id)
   all_data = summary(id)
   return render_template("loan.html", id=id, all_data = all_data)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
