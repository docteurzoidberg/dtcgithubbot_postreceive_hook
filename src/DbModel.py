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
    
class commits(db.Model):
    CommitId = db.StringProperty(required=True) 
    ProjectId = db.StringProperty(required=True)
    RepoName = db.StringProperty()
    RepoUrl = db.StringProperty()
    RepoShortenUrl = db.StringProperty()
    Pusher = db.StringProperty()
    Timestamp = db.StringProperty()
    Message = db.TextProperty()
    CommiterName = db.StringProperty()
    CommiterMail = db.StringProperty()
    CommitUrl = db.StringProperty()
    CommitShortenUrl = db.StringProperty()
    