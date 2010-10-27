#!/usr/bin/env python

import os
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache
from models import State

# def template_values():
# 	values = memcache.get("template_values")
# 	if(values is not None):
# 		return values
# 	
# 	laender = dict([(s.name, s.striking) for s in State.all()])
# 	striking = any(laender.values())
# 	values = {'streik': striking, 
# 		'laender': laender,
# 		'title': title(striking),
# 		'twitter_text': twitter_text(striking)}
# 	
# 	memcache.add("template_values", values)
# 	return values

# TODO: Use Post for toggle and newState
# TODO: Clear memcache.
class ManagerHandler(webapp.RequestHandler):
	def get(self):
		if 'toggle' in self.request.queryvars:
			# Look up state
			# Toggle, save, redirect
			pass
		
		elif 'newState' in self.request.queryvars:
			stateName = self.request.queryvars.get('stateName')
			stateAbbr = self.request.queryvars.get('abbreviation')
			striking = 'striking' in self.request.queryvars
			newState = State(name=stateName, abbreviation=stateAbbr, striking=striking)
			newState.put()
			# redirect
		
		states = list(State.all())
		template_values = {'states': states}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'manager.html')
		self.response.out.write(template.render(path, template_values))

def main():
	application = webapp.WSGIApplication([('/manager/?', ManagerHandler)], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
