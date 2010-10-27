#!/usr/bin/env python

import os
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache
from models import State

class ManagerHandler(webapp.RequestHandler):
	def get_state(self, abbreviation):
		stateQuery = State.all()
		stateQuery.filter("abbreviation =", abbreviation)
		state = stateQuery.get()
		return state

	def post(self):
		action = self.request.POST.get('managerAction')

		if 'toggle' == action:
			state = self.get_state(self.request.POST.get('abbreviation'))
			if state:
				state.striking = not state.striking
				state.put()

		elif 'delete' == action:
			state = self.get_state(self.request.POST.get('abbreviation'))
			if state:
				state.delete()

		elif 'add' == action:
			state = self.get_state(self.request.POST.get('abbreviation'))
			if not state:
				stateName = self.request.POST.get('stateName')
				stateAbbr = self.request.POST.get('abbreviation')
				striking = 'striking' in self.request.POST
				newState = State(name=stateName, abbreviation=stateAbbr, striking=striking)
				newState.put()

		memcache.delete('template_values')
		self.redirect("/manager")

	def get(self):
		states = list(State.all())
		template_values = {'states': states}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'manager.html')
		self.response.out.write(template.render(path, template_values))

def main():
	application = webapp.WSGIApplication([('/manager/?', ManagerHandler)], debug=False)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
