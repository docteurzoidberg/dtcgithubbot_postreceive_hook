from google.appengine.ext import db

class subscribtions(db.Model):
    Mail = db.StringProperty(required=True) 
    RepoName = db.StringProperty(required=True)
    Enabled = db.BooleanProperty(False)
    
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


def delete_subscribtion(email,repo):
        
    subscribtion = subscribtions.get_or_insert(email+"/"+repo, Mail=email, RepoName=repo)
    subscribtion.delete()
  
def delete_subscribtions(email):
        
    for subscribtion in subscribtions.gql("WHERE Mail = :1", email):            
        subscribtion.delete()

def disable_subscriptions(email):
        
    for suscribtion in subscribtions.gql("WHERE Mail = :1", email):            
        suscribtion.Enabled = False
        suscribtion.put()

def disable_subscription(email, repo):
    
    subscribtion = subscribtions.get_or_insert(email+"/"+repo, Mail=email, RepoName=repo)
    subscribtion.Enabled = False
    subscribtion.put()

def enable_subscriptions(email):
    
    for subscribtion in subscribtions.gql("WHERE Mail = :1", email):            
        subscribtion.Enabled = True
        subscribtion.put()

def enable_subscription( email, repo):
    
    subscribtion = subscribtions.get_or_insert(email+"/"+repo, Mail=email,RepoName=repo)
    subscribtion.Enabled = True
    subscribtion.put()