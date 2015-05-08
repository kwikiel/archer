from flask import Flask
from flask import render_template
from investments import loan_chart, get_funded_loans
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/list_loans')
def listing():
   listing = get_funded_loans()
   return render_template("list_loans.html", listing=listing)


@app.route('/loan/<int:id>')
def charts(id):
   loan_chart(id)
   return render_template("loan.html", id=id)

if __name__ == '__main__':
   app.run(debug=True)
