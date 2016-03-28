from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class surveyForm(Form):
	# for page 3
	event = StringField('event', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])
	weather = StringField('weather', validators=[DataRequired()])
	style = StringField('style', validators=[DataRequired()])

class outfitForm(Form):
	# page 1
	outfit_one = TextAreaField('outfit_one', validators=[DataRequired()])
	outfit_two = StringField('outfit_two', validators=[DataRequired()])
	outfit_three = StringField('outfit_three', validators=[DataRequired()])