import json
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import urlfetch



JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

PARENT_KEY = ndb.Key("Entity", "candy_root")

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Client(Model):
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	username = ndb.StringProperty()
	candy = ndb.StringProperty(repeated=True)
	
class Candy(Model):
	name = ndb.StringProperty()
	price = ndb.IntegerProperty()
	
class MainHandler(webapp2.RequestHandler):
	def get(self):
		candy_query = Candy.query(ancestor=PARENT_KEY)
		client_query = Client.query(ancestor=PARENT_KEY)
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(candy=candy_query, client=client_query))
	
	def post(self):
		action = self.request.get("action")
		if action == 'candy':
			new_candy = Candy(parent=PARENT_KEY,
							name = self.request.get("candy_name"),
							price = int(self.request.get("candy_price")))
			new_candy.put()
			self.redirect(self.request.referer)
		else:
			new_client = Client(parent=PARENT_KEY,
								first_name = self.request.get("first_name"),
								last_name = self.request.get("last_name"),
								username = self.request.get("user_name"),
								candy = self.request.get_all("candy[]"))
			key = new_client.put()
			self.redirect(self.request.referer)

class Candy_json(webapp2.RequestHandler):
	def get(self):
		candy_query = Candy.query(ancestor=PARENT_KEY)
		candy_fetch = candy_query.fetch()
		self.response.write(json.dumps([c.to_dict() for c in candy_fetch], indent=4, separators=(',',': ')))



class Client_json(webapp2.RequestHandler):
	def get(self):
		client_query = Client.query(ancestor=PARENT_KEY)
		client_fetch = client_query.fetch()
		self.response.write(json.dumps([c.to_dict() for c in client_fetch], indent=4, separators=(',', ': ')))



class Candy_search(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			candy_query = Candy.query(Candy.name == kwargs['item'])
			candy_fetch = candy_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in candy_fetch], indent=4, separators=(',', ': ')))
	
			
class Client_search(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			client_query = Client.query(Client.username == kwargs['item'])
			client_fetch = client_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in client_fetch], indent=4, separators=(',', ': ')))

class Client_addcandy(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'client' in kwargs:
			client = ndb.Key(Client, (kwargs['client'])).get()
		if 'candy' in kwargs:
			candy_add = ndb.Key(Candy, (kwargs['candy'])).get()
		client.candy.append(candy_add)
		client.put()
		self.response.write(json.dumps(client.to_dict()))
		
class Client_edit(webapp2.RequestHandler):	
	def post(self):
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render())
		
			
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/candy', Candy_json),
	('/client', Client_json),
	('/edit', Client_edit),
], debug=True)
app.router.add(webapp2.Route(r'/candy/<item>', Candy_search))
app.router.add(webapp2.Route(r'/client/<item>', Client_search))
app.router.add(webapp2.Route(r'/client/<client>/<candy>', Client_addcandy))


