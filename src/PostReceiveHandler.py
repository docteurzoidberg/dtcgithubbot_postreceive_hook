# -*- coding: utf-8 -*-
import re
import datetime
import DbModel as db
import Util

import simplejson as json

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class PostReceiveHandler(webapp.RequestHandler):
    
    
        
        
    def post(self):        
        
        
        
        payload = self.request.get('payload')
        
        #log les envois post json
        json_log = db.github_in()
        json_log.When = datetime.datetime.now()
        json_log.Body = payload
        json_log.put()
        
        
        
        # Charge le JSON envoye par github
        githubJson = json.loads(payload)
        
        
        repo_name = githubJson['repository']['name']
        repo_url = githubJson['repository']['url']
        pusher = githubJson['pusher']['name']
        
        commits = githubJson['commits']
                
        message = "*" + pusher + "*" + " a push sur " + repo_url + " !\n"
        
        for commit in commits:
            
            message = message + Util.shorten(commit['url']) + ': '+ commit['message'] + '\n'
                
            for added in commit['added']:
                message = message + "+ " + added + '\n'
                
            for deleted in commit['removed']:
                message = message + "- " + deleted + '\n'
                

        devs = db.developpers.gql("WHERE Active = True")        

        # Recupere le mail de chaque developpeur "actif"
        for dev in devs:
            xmpp.send_message(dev.Mail, message)
       
   
            
    

        

application = webapp.WSGIApplication([('/post-receive', PostReceiveHandler)], debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
