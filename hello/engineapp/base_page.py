import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class HelloWorld(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('page1.html')
		self.response.write(template.render())
	
	def post(self):
		name = self.request.get("user-name")
		sex = self.request.get("sex")
		var = {"username": name,
				"sex": sex}
				
		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render(var))
		