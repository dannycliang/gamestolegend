from flask import render_template, flash, redirect
from app import app
from .forms import *
from .Calculator import *


@app.route('/', methods=['GET', 'POST'])
def index():
    full_form = FullForm()
    games = 0
    game = 0
    goal = ""
    if full_form.rank.data and full_form.validate_on_submit():
        sim = Player(full_form.rank.data, full_form.current_stars.data, full_form.win_streak.data)
        index = 0
        goal = full_form.goal.data
        while index < 1000:
            games += sim.climb_simulation(full_form.goal.data, full_form.winrate.data)
            index += 1
        print(games / 1000)
    return render_template('login.html', games=games / 1000, fform=full_form, goal=goal)
