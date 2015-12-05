from flask import Flask, render_template, redirect
from sqlalchemy import create_engine, MetaData
from flask.ext.login import UserMixin, LoginManager, login_user, logout_user
from flask.ext.blogging import SQLAStorage, BloggingEngine

import controllers
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"  # for WTF-forms and login
app.config["BLOGGING_URL_PREFIX"] = "/blog"
app.config["BLOGGING_DISQUS_SITENAME"] = "Budapest"
app.config["BLOGGING_SITEURL"] = "http://localhost:8000"
app.config["BLOGGING_SITENAME"] = "Travels"

# extensions
engine = create_engine('sqlite:////tmp/blog.db')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=engine)


# user class for providing authentication
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return "Summer Wu"  # typically the user's name

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login/")
def login():
	form = LoginForm()
	if form.validate_on_submit():
	    user = User("admin")
	    login_user(user)
	    flash('Logged in successfully.')
	    next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return abort(400)

        return redirect(next or "/blog/")
	return render_template('login.html', form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/blog/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/yaleims/', defaults={'page': "home", 'sport': ""})
@app.route('/yaleims/<page>', defaults={'sport': ""})
@app.route('/yaleims/<page>/<sport>')
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
	else:
		return render_template('yaleims/%s.html' % page)

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

if __name__ == '__main__':
    app.run(debug=True)
