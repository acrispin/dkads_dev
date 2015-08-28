import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        return self.get_secure_cookie("checking.user")

    def clear_current_user(self):
        self.clear_cookie("checking.user")

    def get_cookie_name(self,name):
        return self.get_cookie(name)

    def set_cookie_name(self,name,value):
        self.set_cookie(name,value)
        
    def clear_cookie_name(self,name):
        self.clear_cookie(name)