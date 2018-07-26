import webapp2

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
    def post(self):
        self.response.headers["Content-Type"] = "application/json"
        # TODO - format? array prob
        indicators = self.request.get ('indicators')
        self.response.write("TODO - api")
        # TODO return json of 'original', 'transformed', 'operation'
        return

app = webapp2.WSGIApplication([
  webapp2.Route(r'/', handler=AboutPage,name = 'about', methods=['GET']),
  webapp2.Route(r'/defang' handler = DefangerPage, name = defangpage,methods=['GET']),
  webapp2.Route(r'/api/defang' handler = DefangerAPI, name = defangapi,methods=['POST']),
], debug=True)