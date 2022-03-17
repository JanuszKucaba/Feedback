"""
An app for collecting opinions of the user of the car service"
heroku application link: https://opel-opinie.herokuapp.com/
"""

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from data import POSTGRESQL_LOCAL, POSTGRESQL_SERVER


app = Flask(__name__)

ENV = 'prod'
#ENV = 'dev'

if ENV == 'dev':
    app.deubg = True
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_LOCAL
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_SERVER

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    """
    Creating table Feedback in PostgreSQL database
    """
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Proszę uzupełnij wymagane pola')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='Już dodałeś komentarz')

@app.route('/opinions')
def opinions():
    import sqlalchemy as db

    if ENV == 'dev':
        engine = db.create_engine(POSTGRESQL_LOCAL)
    else:
        engine = db.create_engine(POSTGRESQL_SERVER)

    conn = engine.connect()
    metadata = db.MetaData()
    opel = db.Table('feedback', metadata, autoload=True, autoload_with=engine)

    query = db.select([opel])

    result_proxy = conn.execute(query)

    result_set = result_proxy.fetchall()
    data = list(result_set)

    return render_template('opinions.html', queries=data)


if __name__ == '__main__':
    app.run()
