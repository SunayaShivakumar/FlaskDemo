from app import db
from app import app

# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(64), index=True, unique=True)

# 	def __repr__(self):
# 		return '<User %r>' % (self.name)

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	link = db.Column(db.String(128), index=True, unique=True)
	# attributes = db.Column(db.String(128))

	def __repr__(self):
		return '<Pic #%r %r of link %r>' % (self.id, self.name, self.link)

class Survey(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# user = 
	event = db.Column(db.String(400))
	location = db.Column(db.String(400))
	weather = db.Column(db.String(400))
	style = db.Column(db.String(400))

	def __repr__(self):
		return '<This is survey #%r \n event: %r \n location: %r \n weather: %r \n style: %r \n>' % (self.id, self.event, self.location, self.weather, self.style)

class Useroutfits(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	outfit_one = db.Column(db.String(700))
	outfit_two = db.Column(db.String(700))
	outfit_three = db.Column(db.String(700))
	
	def __repr__(self):
		return '<These are the outfit descriptions #%r \n one: %r \n two: %r \n three: %r \n>' % (self.id, self.outfit_one, self.outfit_two, self.outfit_three)
