from app import app, blog_engine, login_manager, db
from flask import flash, jsonify, render_template, redirect, request, session
from flask.ext.login import LoginManager, login_user, logout_user
import os

import controllers
from .models import User, Sport
from .forms import LoginForm, SportForm

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/blog/login/", methods=['GET', 'POST'])
def blog_login():
	user = User("admin")
	login_user(user)
	return redirect("/blog")

@app.route("/blog/logout/")
def blog_logout():
	logout_user()
	return redirect("/blog")

@app.route("/yaleims/login/", methods=['GET', 'POST'])
def login():
	if session.get('user'):
		return redirect("/yaleims")
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.passcode.data == app.config['YALE_IMS_PASS']:
			session['user'] = 'admin'
			flash('Logged in successfully.')
			next = request.args.get('next')
			return redirect(next or "/yaleims/admin")
		else:
			flash('Incorrect passcode')
	return render_template('yaleims/login.html', form=form)

@app.route("/yaleims/logout/")
def logout():
	session.pop('user', None)
	return redirect("/yaleims")

@app.context_processor
def added_sports():
	fall_sports = Sport.query.filter_by(season="fall")
	winter_sports = Sport.query.filter_by(season="winter")
	spring_sports = Sport.query.filter_by(season="spring")
	return dict(fall_sports=fall_sports, winter_sports=winter_sports, spring_sports=spring_sports)

@app.route("/yaleims/admin/", methods=['GET', 'POST'])
def admin():
	added_sports = Sport.query.all()
	form = SportForm(request.form)
	if request.method == 'POST':
		# Process data and admin actions
		if form.action.data == "add":
			new_sport = Sport(form.sport.data, form.season.data, form.bk.data, form.br.data, form.cc.data, form.dc.data, form.es.data, form.je.data, form.mc.data, form.pc.data, form.sm.data, form.sy.data, form.tc.data, form.td.data)
			db.session.add(new_sport)
			return redirect("/yaleims/db_sport/" + form.sport.data)
		elif form.action.data == "edit":
			old_sport = Sport.query.filter_by(name=form.sport.data).first()
			old_sport.sport = form.sport.data
			old_sport.season = form.season.data
			old_sport.bk = form.bk.data
			old_sport.br = form.br.data
			old_sport.cc = form.cc.data
			old_sport.dc = form.dc.data
			old_sport.es = form.es.data
			old_sport.je = form.je.data
			old_sport.mc = form.mc.data
			old_sport.pc = form.pc.data
			old_sport.sm = form.sm.data
			old_sport.sy = form.sy.data
			old_sport.tc = form.tc.data
			old_sport.td = form.td.data
		elif form.action.data == "delete":
			old_sport = Sport.query.filter_by(name=form.sport.data).first()
			db.session.delete(old_sport)
		db.session.commit()
		flash('Admin action complete!')
	return render_template('yaleims/admin.html', form=form, added_sports=added_sports)

@app.route('/yaleims/', defaults={'page': "home", 'sport': ""})
@app.route('/yaleims/<page>', defaults={'sport': ""})
@app.route('/yaleims/<page>/<sport>', methods=['GET', 'POST'])
def yaleims(page, sport):
	if page == "home":
		scores = controllers.overall()
		return render_template('yaleims/home.html', scores=scores)
	elif page == "sport":
		sport_names = {
			"c_football": "Coed Football",
			"m_football": "Men's Football",
			"c_soccer": "Coed Soccer",
			"m_soccer": "Men's Soccer",
			"w_soccer": "Women's Soccer",
			"c_tabletennis": "Coed Table Tennis",
			"c_tennis": "Coed Tennis",
			"c_volleyball": "Coed Volleyball"
		}
		scores = controllers.sport(sport)
		return render_template('yaleims/sport.html', sport_name=sport_names[sport], scores=scores)
	elif page == "db_sport":
		scores = controllers.db_sport(sport)
		if request.method == "POST":
			return jsonify(scores)
		else:
			return render_template('yaleims/sport.html', sport_name=sport, scores=scores)
	else:
		return render_template('yaleims/%s.html' % page)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/habitar')
def habitar():
	return render_template('habitar/index.html')

@app.route('/narwhals')
def narwhals():
	return render_template('narwhals/index.html')

@app.route('/v2')
def v2():
	return render_template('homev2.html')

@app.route('/blog')
def blog():
	return redirect("/blog/")

@app.route('/section50')
def section50():
	return render_template('section50.html')

@app.route('/capitalone')
def capitolone():
	posts = controllers.instagram()
	captions = posts['captions']
	likes = posts['likes']
	images = posts['images']
	users = posts['users']
	times = posts['times']
	sentiments = posts['sentiments']
	return render_template('capitalone.html', captions=captions, likes=likes, images=images, users=users, times=times, sentiments=sentiments)

@app.route('/user/<username>')
def hello(username):
	return 'hey %s!' % username