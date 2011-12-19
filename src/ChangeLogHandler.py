# -*- coding: utf-8 -*-


import DbModel as db

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class ChangeLogHandler(webapp.RequestHandler):

    def get(self):        
        
        self.response.headers["Content-Type"] = "text"

        #get repository name in request url (/changelog/reponame.txt)
        repo_name = self.request.path.replace('/changelog/','')
        repo_name = repo_name.replace('.txt','')
        
        #DEBUG
        #self.response.out.write("DEBUG: repo_name = " + repo_name)
        
          
        #get commits for this repo
        commits = db.commits.gql("WHERE RepoName = :1 ORDER BY Timestamp DESC", repo_name)

        #todo: if no commits, return 404
        
        for commit in commits:
            
            self.response.out.write(commit.Timestamp + "; " + commit.Message.replace('\n',' ').replace('\r','') + "\r\n")
        
       
                

    
       
   
            
    

        

application = webapp.WSGIApplication([('/changelog/.*', ChangeLogHandler)], debug=False)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
