from tornado.web import StaticFileHandler
from settings import settings
from handlers.main.home import HomeHandler


url_patterns = [
    (r'/$', HomeHandler),
    (r'/static/(.*)$', StaticFileHandler, dict(path=settings['static_path'])),
    (r'/js/(.*)$', StaticFileHandler, dict(path=settings['static_path'] + '/js')),
    (r'/css/(.*)$', StaticFileHandler, dict(path=settings['static_path'] +'/css')),
    (r'/fonts/(.*)$', StaticFileHandler, dict(path=settings['static_path'] +'/fonts')),
]
