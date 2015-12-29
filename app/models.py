from app import db

from flask.ext.login import UserMixin

class Sport(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	season = db.Column(db.String(10), unique=True)
	bk = db.Column(db.Integer)
	br = db.Column(db.Integer)
	cc = db.Column(db.Integer)
	dc = db.Column(db.Integer)
	es = db.Column(db.Integer)
	je = db.Column(db.Integer)
	mc = db.Column(db.Integer)
	pc = db.Column(db.Integer)
	sm = db.Column(db.Integer)
	sy = db.Column(db.Integer)
	tc = db.Column(db.Integer)
	td = db.Column(db.Integer)

	def __init__(self, name, season, bk, br, cc, dc, es, je, mc, pc, sm, sy, tc, td):
	    self.name = name
	    self.season = season
	    self.bk = bk
	    self.br = br
	    self.cc = cc
	    self.dc = dc
	    self.es = es
	    self.je = je
	    self.mc = mc
	    self.pc = pc
	    self.sm = sm
	    self.sy = sy
	    self.tc = tc
	    self.td = td

	def __repr__(self):
	    return '<Sport %r>' % self.name

# user class for providing authentication
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
