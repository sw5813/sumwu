from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired

class LoginForm(Form):
    passcode = StringField('passcode', validators=[DataRequired()])

class SportForm(Form):
	action = SelectField('action', choices=[('add', 'Add New Sport'), ('edit', 'Edit Sport'), ('delete', 'Delete Sport')], validators=[DataRequired()])
	sport = StringField('sport', validators=[DataRequired()])
	season = SelectField('season', choices=[('fall', 'Fall'), ('winter', 'Winter'), ('spring', 'Spring')], validators=[DataRequired()])
	bk = IntegerField('bk', validators=[DataRequired()])
	tc = IntegerField('tc', validators=[DataRequired()])
	mc = IntegerField('mc', validators=[DataRequired()])
	es = IntegerField('es', validators=[DataRequired()])
	br = IntegerField('br', validators=[DataRequired()])
	sy = IntegerField('sy', validators=[DataRequired()])
	sm = IntegerField('sm', validators=[DataRequired()])
	dc = IntegerField('dc', validators=[DataRequired()])
	je = IntegerField('je', validators=[DataRequired()])
	td = IntegerField('td', validators=[DataRequired()])
	cc = IntegerField('cc', validators=[DataRequired()])
	pc = IntegerField('pc', validators=[DataRequired()])