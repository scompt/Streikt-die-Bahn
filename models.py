from google.appengine.ext import db

class State(db.Model):
    abbreviation = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    striking = db.BooleanProperty(required=True, default=False)
