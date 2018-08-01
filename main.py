# builtins
import re
import os
import logging
import webapp2
import jinja2
import ujson 

# external
import defang


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class DefangerPage (webapp2.RequestHandler):
    def get(self ):
        
        # render client-side
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

    def post(self):
        indicators= self.request.get ("input_text")
        
        # FUTURE - one click copy to clipboard btn
        # FUTURE - save off original to gist if user clicks 'get shareable link'
        # FUTURE - button with 'dangerous' styling to pull the orig content from gist and copy to clipboard
        
        # FUTURE - use JS to call backend 
        # FUTURE - api callable endpoints
            
        # split on comma, whitespace, or newline
        delimiters = "\r\n|,|\ "
        logging.info( re.split (delimiters,indicators) )
        
        # defang each indicator individually, since 'defang' library operates on one at a time
        resp_dict = {"defanged":[] }
        
        for item in re.split (delimiters,indicators):
            resp_dict["defanged"].append(defang.defang(item) )
            
        # render client-side
        template = JINJA_ENVIRONMENT.get_template('index.html')
        return self.response.write(template.render(resp_dict))
        

app = webapp2.WSGIApplication([
  webapp2.Route(r"/", handler = DefangerPage, methods=["GET","POST"]),
])