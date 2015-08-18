'''Minh Nguyen
Assignment 3 part 2: http://assignment3minh.asspot.com
'''

import json
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import urlfetch


PARENT_KEY = ndb.Key("Entity", "candy_root")

class Client(ndb.Model):
	first_name = ndb.StringProperty()
	username = ndb.StringProperty()
	candy = ndb.StringProperty(repeated=True)
	
	
class Candy(ndb.Model):
	name = ndb.StringProperty()
	price = ndb.IntegerProperty()
	
	
class Candy_action(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			candy_query = Candy.query(Candy.name == kwargs['item'])
			candy_fetch = candy_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in candy_fetch], indent=4, separators=(',', ': ')))
		else:
			candy_query = Candy.query(ancestor=PARENT_KEY)
			candy_fetch = candy_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in candy_fetch], indent=4, separators=(',',': ')))
	
	def post(self):
		new_candy = Candy(parent=PARENT_KEY,
					name = self.request.get("candy_name"),
					price = int(self.request.get("candy_price")),
					id = self.request.get("candy_name"))
		key = new_candy.put()
		out = new_candy.to_dict()
		self.response.write(json.dumps(out))
	
	def delete(self, **kwargs):
		if 'item' in kwargs:
			candy_query = Candy.query(Candy.name == kwargs['item'])
			candy = candy_query.get()
			candykey = candy.key.get()
		candykey.key.delete()
		self.response.write("Candy deleted")


class Client_action(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			client_query = Client.query(Client.username == kwargs['item'])
			client_fetch = client_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in client_fetch], indent=4, separators=(',', ': ')))
		else:
			client_query = Client.query(ancestor=PARENT_KEY)
			client_fetch = client_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in client_fetch], indent=4, separators=(',', ': ')))
	
	def post(self):
		new_client = Client(parent=PARENT_KEY,
			username = self.request.get("username"),
			first_name = self.request.get("firstname"),
			candy = self.request.get_all("candy[]"),
			id = self.request.get("username"))
		key = new_client.put()
		out = new_client.to_dict()
		self.response.write(json.dumps(out))
	
	def delete(self, **kwargs):
		if 'item' in kwargs:
			client_query = Client.query(Client.username == kwargs['item'])
			client = client_query.get()
			clientkey = client.key.get()
		clientkey.key.delete()
		self.response.write("Client deleted")
		
class Client_Candy(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'client' in kwargs:
			client_query = Client.query(Client.username == kwargs['client'])
			client = client_query.get()
		if 'candy' in kwargs:
			candy_query = Candy.query(Candy.name == kwargs['candy'])
			candy_add = candy_query.get()
			candy_name = candy_add.name
		client.candy.append(candy_name)
		key = client.put()
		out = client.to_dict()
		self.response.write(json.dumps(out))

app = webapp2.WSGIApplication([
	('/candy', Candy_action),
	('/client', Client_action),
], debug=True)
app.router.add(webapp2.Route(r'/candy/<item>', Candy_action))
app.router.add(webapp2.Route(r'/client/<item>', Client_action))
app.router.add(webapp2.Route(r'/client/<client>/<candy>', Client_Candy))



