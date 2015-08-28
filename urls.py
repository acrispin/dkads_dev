from tornado.web import StaticFileHandler
from settings import settings
from handlers.main.home import HomeHandler
from handlers.report.line import LineHandler
from handlers.report.column import ColumnHandler
from handlers.report.pie import PieHandler


url_patterns = [
    (r'/$', HomeHandler),
    (r'/report/line$', LineHandler),
    (r'/report/column$', ColumnHandler),
    (r'/report/pie$', PieHandler),
    (r'/static/(.*)$', StaticFileHandler, dict(path=settings['static_path'])),
    (r'/js/(.*)$', StaticFileHandler, dict(path=settings['static_path'] + '/js')),
    (r'/css/(.*)$', StaticFileHandler, dict(path=settings['static_path'] +'/css')),
    (r'/fonts/(.*)$', StaticFileHandler, dict(path=settings['static_path'] +'/fonts')),
]
