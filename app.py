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
from utils.env import dsn_dev, dsn_prd, http_port

if __name__ == '__main__':
    try:
        flagport = False
        countargv = len(sys.argv)

        # $ python app.py || $ python app.py 1234 || # $ python app.py d ||  $ python app.py 1234 d
        if countargv >= 2 and sys.argv[1].isdigit():
            port = int(sys.argv[1])
            flagport = True
        else:
            port = http_port            
        
        if (countargv == 2 and sys.argv[1] == 'd') \
           or (countargv == 3 and sys.argv[2] == 'd') :
            dsn = dsn_dev
        else:
            dsn = dsn_prd

        # usado para deployar en heroku y evitar el error : Web process failed to bind to $PORT within 60 seconds of launch
        port = int(os.environ.get('PORT', port))
        
        tornado.web.ErrorHandler = ErrorHandler
        tornado.options.parse_command_line()             

        application = tornado.web.Application(url_patterns, **settings)
        application.db = momoko.Pool(
            dsn = dsn,
            size = 5
        )

        http_server = HTTPServer(application)
        http_server.listen(port, '0.0.0.0')

        print "Iniciando app en", port
        print "dsn", dsn

        IOLoop.instance().start()

    except KeyboardInterrupt:
        print 'Aborted'