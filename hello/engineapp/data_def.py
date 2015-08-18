from google.appengine.ext import ndb

class Player(ndb.Model):
	name = ndb.StringProperty(required=True)
	sex = ndb.StringProperty(required=True)
	OS = ndb.StringProperty(required=True)
	games = ndb.StringProperty(repeated=True)
	text = ndb.TextProperty(required=True)