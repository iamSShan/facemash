#!/usr/bin/env python
import os
import sys
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from utility.elo import Elo
from sqlalchemy import desc


app = Flask(__name__)
# Testing database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mash_user:root@localhost/mash_db'
# Production database URI
app.config['DATABASE_URL'] = 'postgres://jnshsfpzctixno:cd9d471dab1c578f4b6cdceb5c6964b931ea953bea950b900769a1568ba0dd01@ec2-52-73-247-67.compute-1.amazonaws.com:5432/d2bep9ila9jgpu'
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
        # As everytime data from db is deleted in postgres, it's id sequence number next time start from last updated + 1 
        # So allow sequence number to start from 1 only
        # db.session.execute('ALTER SEQUENCE "contestant_id_seq" RESTART WITH 1')
        # db.session.execute('ALTER TABLE `contestant` AUTO_INCREMENT = 1;')
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()
        return render_template('db_response.html', success=False)

    # For local:
    # images_location = 'static/images/'
    # For Production:
    images_location = 'masher/static/images/'
    for image in os.listdir(images_location):
        # image_path = os.path.abspath(image)
        try:
            file_name_list = image.split('-')
            # As .gitkeep file is not to be included
            if '.gitkeep' in file_name_list:
                continue

            name = file_name_list[0] + " " + file_name_list[1]
            # Populate db
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
    print total_count
    # Get random number b/w 1 and total count
    rand = random.randrange(1, total_count+1)
    # Get contestant at that index
    contestant = Contestant.query.get(rand)
    print contestant

    return contestant


@app.route('/start/', methods=["GET", "POST"])
def start():
    if request.method == "GET":
        contestants = [get_random_contestant(), get_random_contestant()]
        # print contestants
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


@app.route('/ranking/<int:user_id>')
def show_ranking(user_id):
    selected_contestant = Contestant.query.get(user_id)
    all_contestants = Contestant.query.order_by(desc(Contestant.rating)).all()

    return render_template("ranking.html", selected_contestant=selected_contestant,
                           all_contestants=all_contestants)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404)    


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message=e, error_code=500)


if __name__ == "__main__":
    app.run(debug=True)

