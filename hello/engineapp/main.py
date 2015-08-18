import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
	
		
class Enter(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('enter.html')
		self.response.write(template.render())
		
class View(webapp2.RequestHandler):
	def post(self):
		var = {'name': self.request.get("user-name"),
				'sex': self.request.get("sex"),
				'OS': self.request.get("OS"),
				'games': self.request.get_all("games[]"),
				'text': self.request.get("text")
				}
		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render(var))
	
class Edit(webapp2.RequestHandler):
	def post(self):
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		var = {'name': self.request.get("user-name"),
				'sex': self.request.get("sex"),
				'OS': self.request.get("OS"),
				'games': self.request.get_all("games[]"),
				'text': self.request.get("text")
				}
		self.response.write(template.render(var))
	
		
app = webapp2.WSGIApplication([
		('/', Enter), 
		('/edit', Edit),
		('/view', View),
		], debug=True)

