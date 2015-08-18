##Author: Minh Nguyen
##CS 496: Creating a cloud back-end with Python on Google App Engine

import webapp2
import json
from google.appengine.ext import ndb

PARENT_KEY = ndb.Key("Entity", "root")

class User(ndb.Model):
	username = ndb.StringProperty()
	password = ndb.StringProperty()
	class_teach = ndb.StringProperty(repeated=True)

class Class(ndb.Model):
	classname = ndb.StringProperty()
	class_size = ndb.IntegerProperty()
	student = ndb.StringProperty(repeated=True)

class Student(ndb.Model):
	studentname = ndb.StringProperty()
	
class User_action(webapp2.RequestHandler):
	pass
	#def post(self, **kwargs):
		#new_user = User(parent=PARENT_KEY,
		#	username = self.request.get("username"),
		#	password = self.request.get("password"),
		#	class_teach = 
	
class Student_action(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			student_query = Student.query(Student.studentname == kwargs['item'])
			student_fetch = student_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in student_fetch], indent=4, separators=(',',': ')))
		else:	
			student_query = Student.query(ancestor=PARENT_KEY)
			student_fetch = student_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in student_fetch], indent=4, separators=(',',': ')))
	
	def post(self, **kwargs):
		new_student = Student(parent=PARENT_KEY,
					  studentname = self.request.get("studentname"),
					  id = self.request.get("studentname"))
		key = new_student.put()
		out = new_student.to_dict()
		self.response.write(json.dumps(out))
		
	def delete(self, **kwargs):
		if 'item' in kwargs:
			student_query = Student.query(Student.studentname == kwargs['item'])
			student = student_query.get()
			studentkey = student.key.get()
		studentkey.key.delete()
		self.response.write("Student deleted")
		
class Class_action(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			class_query = Class.query(Class.classname == kwargs['item'])
			class_fetch = class_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in class_fetch], indent=4, separators=(',',': ')))
		else:
			class_query = Class.query(ancestor=PARENT_KEY)
			class_fetch = class_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in class_fetch], indent=4, separators=(',',': ')))
	
	def post(self):
		new_class = Class(parent=PARENT_KEY,
					classname = self.request.get("classname"),
					class_size = int(self.request.get("class_size")),
					student = self.request.get_all("student[]"),
					id = self.request.get("classname"))
		key = new_class.put()
		out = new_class.to_dict()
		self.response.write(json.dumps(out))
	
	def delete(self, **kwargs):
		if 'item' in kwargs:
			class_query = Class.query(Class.classname == kwargs['item'])
			class_class = class_query.get()
			classkey = class_class.key.get()
		classkey.key.delete()
		self.response.write("Class deleted")

class User_action(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'item' in kwargs:
			user_query = User.query(User.username == kwargs['item'])
			user_fetch = user_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in user_fetch], indent=4, separators=(',',': ')))
		else:
			user_query = User.query(ancestor=PARENT_KEY)
			user_fetch = user_query.fetch()
			self.response.write(json.dumps([c.to_dict() for c in user_fetch], indent=4, separators=(',',': ')))
	
	def post(self):
		new_user = User(parent=PARENT_KEY,
					username = self.request.get("username"),
					password = self.request.get("password"),
					class_teach = self.request.get_all("classes[]"),
					id = self.request.get("username"))
		key = new_user.put()
		out = new_user.to_dict()
		self.response.write(json.dumps(out))
		
	
			

class User_Class(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'user' in kwargs:
			user_query = User.query(User.username == kwargs['user'])
			user = user_query.get()
		if 'class' in kwargs:
			class_query = Class.query(Class.classname == kwargs['class'])
			class_add = class_query.get()
			class_name = class_add.classname
		user.class_teach.append(class_name)
		key = user.put()
		out = user.to_dict()
		self.response.write(json.dumps(out))
		
	def delete(self, **kwargs):
		if 'user' in kwargs:
			user_query = User.query(User.username == kwargs['user'])
			user = user_query.get()
		if 'class' in kwargs:
			class_query = Class.query(Class.classname == kwargs['class'])
			class_remove = class_query.get()
			class_name = class_remove.classname
		user.class_teach.remove(class_name)
		key = user.put()
		out = user.to_dict()
		self.response.write(json.dumps(out))

class Class_Student(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'class' in kwargs:
			class_query = Class.query(Class.classname == kwargs['class'])
			class_class = class_query.get()
		if 'student' in kwargs:
			student_query = Student.query(Student.studentname == kwargs['student'])
			student_add = student_query.get()
			student_name = student_add.studentname
		class_class.student.append(student_name)
		key = class_class.put()
		out = class_class.to_dict()
		self.response.write(json.dumps(out))
			
	
	

app = webapp2.WSGIApplication([
    ('/user', User_action),
	('/student', Student_action),
	('/class', Class_action),
], debug=True)
app.router.add(webapp2.Route(r'/user/<item>', User_action))
app.router.add(webapp2.Route(r'/student/<item>', Student_action))
app.router.add(webapp2.Route(r'/class/<item>', Class_action))
app.router.add(webapp2.Route(r'/user/<user>/<class>', User_Class))
app.router.add(webapp2.Route(r'/class/<class>/<student>', Class_Student))