from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class surveyForm(Form):
	# for page 3
	event = TextAreaField('event', validators=[DataRequired()])
	location = TextAreaField('location', validators=[DataRequired()])
	weather = TextAreaField('weather', validators=[DataRequired()])
	style = TextAreaField('style', validators=[DataRequired()])

class outfitForm(Form):
	# page 1
	outfit_one = TextAreaField('outfit_one', validators=[DataRequired()])
	outfit_two = TextAreaField('outfit_two', validators=[DataRequired()])
	outfit_three = TextAreaField('outfit_three', validators=[DataRequired()])