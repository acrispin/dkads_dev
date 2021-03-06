import tornado.web
import os
import httplib

class ErrorHandler(tornado.web.RequestHandler):
    """Generates an error response with status_code for all requests."""
    def __init__(self, application, request, status_code):
        tornado.web.RequestHandler.__init__(self, application, request)
        self.set_status(status_code)
    
    def write_error(self, status_code, **kwargs):
        self.require_setting("static_path")
        if status_code in [404, 500, 503, 403]:
            filename = os.path.join(self.settings['static_path'], '%d.html' % status_code)
            if os.path.exists(filename):
                f = open(filename, 'r')
                data = f.read()
                f.close()
                self.write(data)
        self.write("<html><title>%(code)d: %(message)s</title>" \
                    "<body class='bodyErrorPage'><h1>%(code)d: %(message)s</h1></body></html>" % {
                    "code": status_code,
                    "message": httplib.responses[status_code],
                })
    
    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)