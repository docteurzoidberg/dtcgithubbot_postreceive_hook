import DbModel as db
import datetime
import re

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class XMPPHandler(webapp.RequestHandler):
    
    def unwatch_command(self, email, repo):
          
        if(repo == ""):
            db.delete_subscribtions(email)
            message = "All your subscribtions were removed from database !"
        else:
            db.delete_subscribtion(email,repo)
            message = "The repository is not watched anymore !"

        xmpp.send_message(email, message)
        
        
    def watch_command(self, email, repo):
          
        db.enable_subscription(email, repo)
        message = "You subscribed to the " + repo + " repository !"
        
        xmpp.send_message(email, message)

    def mute_command(self, email, repo):
               
        if(repo == ""):
            db.disable_subscriptions(email)
            message = "All repositories you subscribed are now muted !"
        else:
            db.disable_subscription(email,repo)
            message = "The repository " + repo + " is now muted !"
            
        xmpp.send_message(email,message)

    def unmute_command(self, email, repo):
        
        if(repo == ""):
            db.enable_subscriptions(email);
            message = "All repositories you subscribed are now unmuted !"
        else:
            db.enable_subscription(email, repo)
            message = "Repository " + repo + " is now unmuted !"
        
        xmpp.send_message(email, message)
  
     
    def post(self):
        
        message = xmpp.Message(self.request.POST)
        
        #DEBUG: log xmmp input
        log_xmpp_in = db.xmpp_in(From = message.sender)
        log_xmpp_in.Body = message.body
        log_xmpp_in.When = datetime.datetime.now()
        log_xmpp_in.put()
        
        
        #Split message body into args array
        args = message.body.split(" ")
        command = args[0]
        
        
        #try to read parameters ?
        try:
            repo = args[1]
        except IndexError:
            repo = ""
        
        
        
        #Parse sender JID to extract email        
        email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        result = email_pattern.match(message.sender)
        email = result.group(0)

        if(command=='!mute'):
            #mute (or stop watching) all or one repository
            self.mute_command(email, repo)
        elif(command=='!unmute'):
            #unmute (or start watching) all or one repository
            self.unmute_command(email, repo)        
        elif(command=='!watch'):
            #start watching one repository
            self.watch_command(email, repo)
        elif(command=='!unwatch'):
            #stop watching one/all repository
            self.unwatch_command(email, repo)
        else:
            #Display usage if unkown command
            usage = "Watch command:\n"
            usage += "    !watch  %repo_name%    -> start watching this repository\n"
            usage += "Unmute command:\n"
            usage += "    !unmute    -> unmute notifications about all previously watched repositories\n"
            usage += "    !unmute %repo_name%     -> unmute notifications about this repository or start watching it\n"
            usage += "Mute command:\n"
            usage += "    !mute     -> mute notifications about all watched repositories\n"
            usage += "    !mute %RepoName%    -> mute notifications about this repository\n"
            
            xmpp.send_message(message.sender, "Unknown command: " + command + "\n" + usage)
          
xmpp_application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)], debug=True)

def main():
    run_wsgi_app(xmpp_application)
    
if __name__ == "__main__":
    main()