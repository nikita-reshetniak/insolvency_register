from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scrap import parser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles.db'
db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    dates = db.relationship('Date', backref='profile')

    def __repr__(self):
        return 'Profile ' + str(self.id)

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profiles', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = datetime.strptime(request.form['birth_date'], '%d.%m.%Y')
        new_profile = Profile(first_name=first_name, last_name=last_name, birth_date=birth_date)
        db.session.add(new_profile)
        db.session.commit()

        dates = parser(first_name, last_name, request.form['birth_date'])
        for date in dates:
            new_date = Date(date=datetime.strptime(date, '%d.%m.%Y'), profile_id=new_profile.id)
            db.session.add(new_date)
            db.session.commit()

        # db.session.add(Date(date=datetime.strptime(request.form['birth_date'], '%d.%m.%Y'), profile_id=new_profile.id))
        # db.session.commit()

        return redirect('/profiles')
    else:
        all_profiles = Profile.query.all()
        all_dates = Date.query.all()
        return render_template('profiles.html', profiles=all_profiles, dates=all_dates)


@app.route('/profiles/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        return redirect('/profiles')
    else:
        return render_template('new_profile.html')

@app.route('/profiles/load', methods=['GET', 'POST'])
def load_csv():
    if request.method == 'POST':
        # profile.first_name = request.form['first_name']
        # profile.last_name = request.form['last_name']
        # profile.birth_date = request.form['birth_date']
        # new_profile = Profile(first_name=first_name, last_name=last_name, birth_date=birth_date)
        # db.session.add(new_profile)
        # db.session.commit()

        # dates = parser()
        # for date in dates:
        #     new_date = Date(date=date, profile_id=1)
        #     db.session.add(new_date)
            
        # db.session.add(Date(date=datetime.strptime(request.form['birth_date'], '%d.%m.%Y'), profile_id=1))
        # db.session.commit()
        
        return redirect('/profiles')
    else:
        return render_template('load_csv.html')


@app.route('/profiles/load/get-csv', methods=['GET', 'POST'])
def get_csv():
    return send_file('/static/client/template.csv', attachment_filename='template.csv')


@app.route('/profiles/delete/<int:id>')
def delete(id):
    profile = Profile.query.get_or_404(id)
    db.session.delete(profile)
    db.session.commit()

    return redirect('/profiles')


if __name__ == '__main__':
    app.run(debug=True)