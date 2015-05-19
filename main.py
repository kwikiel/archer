from flask import Flask
from flask import render_template, url_for
from investments import loan_chart, get_funded_loans, weird
from agregate import *
from operator import itemgetter
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
#Meh
@app.route('/shark')
def shark():
   loans = get_funded_loans()
   levelup = []
   for loan in loans:
      levelup.append([(summary(loan)['real_rate']), summary(loan)['id']])
   return render_template("shark.html", loans_list = levelup)


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
   app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
