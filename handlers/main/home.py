from handlers.base import BaseHandler
import utils.logginghandler as mylogger
from utils.functions import custom_log

class HomeHandler(BaseHandler):
    def get(self):
        #mylogger.info(custom_log(self.request))        
        self.render("main/index.html", **{})