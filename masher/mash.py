import os
import sys
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from utility.elo import Elo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test_user:root@localhost/mash_db'
# Initiate a DB object
db = SQLAlchemy(app)

class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Using image path instead of image here
    image = db.Column(db.String(264), unique=True) #absolute path to file
    name = db.Column(db.String(80), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=100)
    wins = db.Column(db.Integer, default=0)
    matches = db.Column(db.Integer, default=0)

    __tablename__ = 'contestant'

    def __repr__(self):
        return '<Contestant %r>' % self.name


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/database/frequentare/')
def populate_db():
    """
    Populate DB
    """
    db.create_all()
    db.session.commit()
    try:
        # Delete existing rows if any
        db.session.query(Contestant).delete()
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()
        return render_template('db_response.html', success=False)

    for image in os.listdir('static/images/'):
        # image_path = os.path.abspath(image)
        file_name_list = image.split('-')
        name = file_name_list[0] + " " + file_name_list[1]
        # Populate db
        try:
            new_contestant = Contestant(name=name, image=image)
            db.session.add(new_contestant)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            return render_template('db_response.html', success=False)

    return render_template('db_response.html', success=True)
    


def get_random_contestant():
    # Get total count
    total_count = Contestant.query.count()
    # Get random number b/w 1 and total count
    rand = random.randrange(1, total_count+1)
    # Get contestant at that index
    contestant = Contestant.query.get(rand)

    return contestant


@app.route('/start/', methods=["GET", "POST"])
def start():
    if request.method == "GET":
        contestants = [get_random_contestant(), get_random_contestant()]
        # Both contestant should not be same
        while contestants[0].id == contestants[1].id:
            contestants[1] = get_random_contestant()
        return render_template("main.html", contestants=contestants)

    if request.method == "POST":
        first_contestant_submit = request.form.get('first_contestant_submit')
        second_contestant_submit = request.form.get('second_contestant_submit')
        first_contestant_id = request.form.get('first_contestant')
        second_contestant_id = request.form.get('second_contestant')
        first_contestant = Contestant.query.get(first_contestant_id)
        second_contestant = Contestant.query.get(second_contestant_id)

        if first_contestant_submit:
            winner_contestant = 1
        else:
            winner_contestant = 2

        # Use Elo rating algorithm
        elo = Elo()
        rating1, rating2 = elo.give_rating(first_contestant.rating, second_contestant.rating, winner_contestant)
        first_contestant.rating = rating1
        second_contestant.rating = rating2
        db.session.commit()
        return redirect(url_for('start'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404)    


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message=e, error_code=500)


if __name__ == "__main__":
    app.run(debug=True)

