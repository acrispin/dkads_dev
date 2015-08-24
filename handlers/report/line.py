from handlers.base import BaseHandler
import utils.logginghandler as mylogger
from utils.functions import custom_log

class LineHandler(BaseHandler):
    def get(self):
        #mylogger.info(custom_log(self.request))        
        self.render("report/line.html", **{})