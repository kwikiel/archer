from flask import Flask
from flask import render_template
from investments import loan_chart
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/loan/<int:id>')
def charts(id):
   loan_chart(id)
   return render_template("loan.html", id=id)

if __name__ == '__main__':
   app.run(debug=True)
