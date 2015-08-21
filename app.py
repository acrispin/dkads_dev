import tornado.web
import tornado.options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import momoko

from settings import settings
from urls import url_patterns
from handlers.error import ErrorHandler
from utils.env import dsn, http_port

if __name__ == '__main__':
    try:
        tornado.web.ErrorHandler = ErrorHandler
        tornado.options.parse_command_line()             

        application = tornado.web.Application(url_patterns, **settings)
        application.db = momoko.Pool(
            dsn = dsn,
            size = 5
        )
        http_server = HTTPServer(application)
        http_server.listen(http_port, '0.0.0.0')

        print "Iniciando app en", http_port

        IOLoop.instance().start()

    except KeyboardInterrupt:
        print 'Aborted'