import os
import sys
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

        if len(sys.argv) == 2 and sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            port = http_port

        # usado para deployar en heroku y evitar el error : Web process failed to bind to $PORT within 60 seconds of launch
        port = int(os.environ.get('PORT', port))
        
        http_server = HTTPServer(application)
        http_server.listen(port, '0.0.0.0')

        print "Iniciando app en", port

        IOLoop.instance().start()

    except KeyboardInterrupt:
        print 'Aborted'