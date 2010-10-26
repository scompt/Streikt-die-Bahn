#!/usr/bin/env python

import os
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache
from models import State

def title(striking):
	if striking:
		return "Streikt die Bahn? - Ja"
	else:
		return "Streikt die Bahn? - Nein"

def twitter_text(striking):
	if striking:
		return "Die Bahn streikt schonwieder!"
	else:
		return "Die Bahn streikt grad nicht!"

def template_values():
	values = memcache.get("template_values")
	if(values is not None):
		return values
	
	laender = dict([(s.name, s.striking) for s in State.all()])
	striking = any(laender.values())
	values = {'streik': striking, 
		'laender': laender,
		'title': title(striking),
		'twitter_text': twitter_text(striking)}
	
	memcache.add("template_values", values)
	return values

class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
		self.response.out.write(template.render(path, template_values()))

class JsonHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(json.dumps(template_values()))

class ManagerHandler(webapp.RequestHandler):
	def get(self):
		s = State(name="Bayern", abbreviation="BY", striking = False)
		s.put()
		memcache.delete("template_values")
		self.response.out.write("asdf")

def main():
	application = webapp.WSGIApplication([('/', MainHandler), ('/streik.json', JsonHandler), ('/manager/', ManagerHandler)], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
