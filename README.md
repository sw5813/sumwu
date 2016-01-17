personal site/project playground
====================

### To run locally:
1. Start the virtual environment: source venv/bin/activate
2. Start the server: python hello.py
3. Check it out in a browser at: http://127.0.0.1:5000/
	- Yale IMs site located at: http://127.0.0.1:5000/yaleims
	- #CapitalOne Instagram project located at: http://127.0.0.1:5000/capitalone
	- Blog at: http://127.0.0.1:5000/blog

### Pushing to production:
1. After pushing the latest version to github, push it to heroku: git push heroku master
2. Visit the site at: https://sumwu.me/
	- Yale IMs site at: https://sumwu.me/yaleims
	- #CapitalOne Instagram project at https://sumwu.me/capitalone
	- Blog at: https://sumwu.me/blog

### To do:
* Look into utilizing Flask-Cache in blog
* If people actually start using it, spin off Yale IMs as a separate repo

### Notes:
* No real users, just a session code check
* Local database info:
	basedir = os.path.abspath(os.path.dirname(__file__))
	print('sqlite:///' + os.path.join(basedir, 'app.db'))
