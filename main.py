# builtins
import webapp2
import urllib
import ujson #goog decided to rewrite the py lib for some reason?

# external
import defang

class DefangerPage (webapp2.RequestHandler):
    def get(self ):
        # FUTURE - use jinja/template
        self.response.headers["Content-Type"] = "text/html"
        html = """
        <html>
        <body>
        <form action="/api/defang" method="post">
        <div><input type="text" name = 'indicator' placeholder="Your indicator" /></div>
        <div><input type="submit" value="defang / refang me" </div>

        </form>
        <p> online defanger (and refanger) for indicators - <a href="https://pypi.org/project/defang/"> Powered by python/defang </a></p> 
        </body>
        </html>
        """
        
        self.response.write(html)

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
            
        return self.response.write(ujson.dumps(resp_dict))
        

app = webapp2.WSGIApplication([
  webapp2.Route(r"/", handler = DefangerPage, methods=["GET"]),
  webapp2.Route(r"/api/defang", handler = DefangerAPI,methods=["POST"])
])