from google.appengine.ext import db

class developpers(db.Model):
    Mail = db.StringProperty(required=True)
    Active = db.BooleanProperty(False)
    
class xmpp_in(db.Model):
    From = db.StringProperty(required=True)
    Body = db.TextProperty()
    When = db.DateTimeProperty()

class github_in(db.Model):
    When = db.DateTimeProperty()
    Body = db.TextProperty()