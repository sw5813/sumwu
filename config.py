import os
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY'] # for WTF-forms and login
BLOGGING_URL_PREFIX = "/blog"
BLOGGING_DISQUS_SITENAME = "A small girl in a big world"
BLOGGING_SITEURL = "http://localhost:5000"
BLOGGING_SITENAME = "A small girl in a big world"

YALE_IMS_PASS = os.environ['YALE_IMS_PASS']
BLOG_PASS = os.environ['BLOG_PASS']
