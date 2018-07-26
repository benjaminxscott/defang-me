# builtins
import webapp2
import urllib

# external
import defang

class AboutPage (webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("online defanger - powered by <a href=https://pypi.org/project/defang/ python/defang>")

class DefangerPage (webapp2.RequestHandler):
    def get(self ):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("<b>TODO - form</b>")

class DefangerAPI (webapp2.RequestHandler):
        # FUTURE - refactor to endpoints
    def post(self):
        self.response.headers["Content-Type"] = "application/json"
        # FUTURE - refactor to array/bulk
        indicator= self.request.get ("indicator")
        operation = "defang"
        refang = False
        
        if "[" in indicator:
            operation = "refang"
            refang = True
            
        # defang each indicator individually, since lib function takes one at a time
        resp_dict = {"orig": indicator,"op":operation}
        
        if refang:
            resp_dict["transformed"] = defang.refang(indicator)
        else:
            resp_dict["transformed"] = defang.defang(indicator)
            
        return self.response.write(resp_dict)
        

app = webapp2.WSGIApplication([
    # TODO setup tls w/ schemes=["https"] and LE cert
  webapp2.Route(r"/", handler=AboutPage,name = "about", methods=["GET"]),
  webapp2.Route(r"/defang", handler = DefangerPage, methods=["GET"]),
  webapp2.Route(r"/api/defang", handler = DefangerAPI,methods=["POST"])
])