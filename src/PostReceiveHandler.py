# -*- coding: utf-8 -*-

import datetime
import DbModel as db
import Util

import simplejson as json

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class PostReceiveHandler(webapp.RequestHandler):
    
    def handle_github_json(self, project, githubjson):

        repo_name = githubjson['repository']['name']
        repo_url = githubjson['repository']['url']
        pusher = githubjson['pusher']['name']
        
        commits = githubjson['commits']
                
        #prepare message string for xmpp
        message = "*" + pusher + "*" + " a push sur " + repo_url + " !\n"
        
        for commit in commits:
            
            
            dbcommit = db.commits(CommitId = commit['id'], ProjectId = project)
            dbcommit.Pusher = pusher
            dbcommit.ProjectId = project
            dbcommit.CommitId = commit['id']
            dbcommit.CommitUrl = commit['url']
            dbcommit.RepoName =  repo_name
            dbcommit.RepoUrl =  repo_url
            dbcommit.RepoShortenUrl =  Util.shorten(repo_url)
            dbcommit.CommiterName =  commit['author']['name']
            dbcommit.CommiterMail =  commit['author']['email']
            dbcommit.CommitShortenUrl = Util.shorten(commit['url'])
            dbcommit.Message = commit['message']
            dbcommit.Timestamp = commit['timestamp']
            
            #insert commit infos into database
            dbcommit.put()
            
            message = message + dbcommit.CommitShortenUrl + ': '+ dbcommit.Message + '\n'
                
            for added in commit['added']:
                message = message + "+ " + added + '\n'
                
            for deleted in commit['removed']:
                message = message + "- " + deleted + '\n'
       
            
        
        
        
        #get developpers and send them a xmpp notification
        devs = db.developpers.gql("WHERE Active = True")        

        # Recupere le mail de chaque developpeur "actif"
        for dev in devs:
            xmpp.send_message(dev.Mail, message)
        
    
        
    def post(self):        
        
        
        #get project id in request url (/post-receive/projectid)
        projectid = self.request.path.replace('/post-receive/','')
        
        #if no project id, switch to default one
        if(projectid=='/post-receive'):
            projectid='default'
            
        
        #github's payload is stored in a post variable called "payload"
        githubpayload = self.request.get('payload')
        
        
        #DEBUG: log json data "as is", create new db entry
        db_log_payload = db.github_in()
        db_log_payload.When = datetime.datetime.now()
        db_log_payload.Body = githubpayload
        db_log_payload.put()
        
        
        
        # Charge le JSON envoye par github
        githubjson = json.loads(githubpayload)
        
        self.handle_github_json(projectid, githubjson)
        
        
       
                

    
       
   
            
    

        

application = webapp.WSGIApplication([('/post-receive', PostReceiveHandler),('/post-receive/.*', PostReceiveHandler)], debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
