from tornado import gen, escape
import momoko
from handlers.base import BaseHandler
from utils.functions import verify_password

class AuthLoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)

    @gen.coroutine
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        try:
            cursor = yield momoko.Op(self.db.execute, "select password,name,rol from sy_user where email = '%s'" % (username,))
            usuario = cursor.fetchone()
            cursor.close()
            hashed_pwd = usuario[0]
        except Exception as e:
            print "auth failure: " + str(e)
            auth = False
        else:
            auth = verify_password(password, hashed_pwd)
        if auth:
            self.set_current_user(username)            
            self.redirect(self.get_argument("next", u"/dashboard/"))
        else:
            error_msg = u"?error=" + escape.url_escape("Login incorrecto")
            self.redirect(u"/auth/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("checking.user", escape.json_encode(user))
        else:
            self.clear_cookie("checking.user")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_current_user()
        self.redirect(u"/auth/login/")
