import DbModel as db
import datetime
import re

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class XMPPHandler(webapp.RequestHandler):
    
    def post(self):
        
        message = xmpp.Message(self.request.POST)
        
        
        
        email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        result = email_pattern.match(message.sender)
        mail = result.group(0)
        
        keyname = mail
        
        e = db.developpers.get_or_insert(keyname, Mail=mail)
        
        if(message.body=='!unmute'):
            
            e.Active = True
            e.put()

        elif(message.body=='!mute'):
            
            e.Active = False
            e.put()           
            
        else:
            
            f = db.xmpp_in(From = message.sender)
            f.Body = message.body
            f.When = datetime.datetime.now()
            f.put()
        
        
            
xmpp_application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)], debug=True)

def main():
    run_wsgi_app(xmpp_application)
    
if __name__ == "__main__":
    main()