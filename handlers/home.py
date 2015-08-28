from handlers.base import BaseHandler
import utils.logginghandler as mylogger
from utils.functions import custom_log

class MainHandler(BaseHandler):
    def get(self):
        #mylogger.info('pagina de inicio test')        
        #mylogger.info(repr(self.request))        
        mylogger.info(custom_log(self.request))        
        self.render("index.html", **{})