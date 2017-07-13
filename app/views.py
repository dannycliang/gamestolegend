from flask import render_template, flash, redirect
from app import app
from .forms import *
from .League import *
from .Summoner import *


@app.route('/')


@app.route('/index', methods=['GET', 'POST'])
def index():
    full_form = FullForm()
    abridged_form = AbridgedForm()
    games = 0
    game = 0
    goal = ""
    if full_form.rank.data and full_form.validate_on_submit():
        sim = Player(full_form.rank.data, full_form.current_gain.data, full_form.current_loss.data, full_form.current_LP.data, full_form.in_series.data, full_form.series_wins.data, full_form.series_losses.data)
        index = 0
        goal = full_form.goal.data
        while index < 1000:
            games += sim.Ranked_calculate(full_form.goal.data, full_form.winrate.data)
            index += 1
    elif abridged_form.username.data and abridged_form.validate_on_submit():
        url_open(abridged_form.username.data)
        info = get_info()
        sim = Player(info[0], info[3], 40 - info[3], int(info[1]), info[4], 0, 0)
        goal = abridged_form.goal.data
        index = 0
        while index < 1000:
            games += sim.Ranked_calculate(abridged_form.goal.data, int(info[2]))
            index += 1
    return render_template('login.html', games=games // 100, fform=full_form, aform=abridged_form, goal=goal)
