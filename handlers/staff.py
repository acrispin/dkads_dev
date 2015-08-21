from tornado import gen, web
import momoko
import time
import simplejson
from handlers.base import BaseHandler
from utils.functions import pwgen
from utils import security, qrgen
import utils.logginghandler as mylogger

class DealerHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user where email = '%s'" % (email,))
            user_array = cursor_user.fetchone()
            # either we call to fetchall and consume all or close the cursor
            # otherwise transaction is still opened and create conflicts later
            # with the one below
            cursor_user.close()
            rol, user_name = '',''
            if not user_array:
                 self.redirect(u"/auth/login/")
                 return
            else:
                rol = user_array[0]
                user_name = user_array[1]
            if rol == '':
                self.clear_current_user()
                self.redirect(u"/auth/login/")
            else:
                # condicion adicionada para restringir el acceso a otros usuarios que no tengan el rol de staff
                if rol != "staff":
                    self.redirect(u"/auth/login/")
                    return
                # NOTE: USER_NAME, EMAIL and ROL are rendered in an %include%
                # within dealer.html
                # TODO: dealers = "select name, email from sy_user where rol='distribuitor'"
                cursor = yield momoko.Op(self.db.execute, "SELECT email,name \
                                          from sy_user where rol='dealer'")
                dealers = cursor.fetchall()
                self.render("dealer.html", **dict(user_name=user_name,
                                                email=email,
                                                rol=rol,
                                                dealers=dealers))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})



class NewDealerHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user where email = '%s'" % (email,))
            user_array = cursor_user.fetchone()
            cursor_user.close()
            rol, user_name = '',''
            if not user_array:
                 self.redirect(u"/auth/login/")
                 return
            else:
                rol = user_array[0]
                user_name = user_array[1]
            if rol == '':
                self.clear_current_user()
                self.redirect(u"/auth/login/")
            else:
                # condicion adicionada para restringir el acceso a otros usuarios que no tengan el rol de staff
                if rol != "staff":
                    self.redirect(u"/auth/login/")
                    return
                self.render("newdealer.html", **dict(user_name=user_name,
                                                    email=email,
                                                    rol=rol))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})


    @gen.coroutine
    @web.authenticated
    def post(self):
        connection = None
        try:
            current_user = self.get_current_user()
            stmt = "INSERT INTO sy_user (email, password, name, rol, \
                    is_salecompany, is_active, created_by, created_on) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"
            name = self.get_argument("dealername")
            phone = self.get_argument("dealerphone")
            email = self.get_argument("dealermail")
            is_active = True if self.get_argument("dealeractive", "") else False
            can_sell_comp = True if self.get_argument("dealercanselltocomp", "") else False
            temp_passwd = pwgen()
            hashed_passwd = security.pwd_context.encrypt(temp_passwd)
            connection = yield momoko.Op(self.db.getconn)
            with self.db.manage(connection):
                yield momoko.Op(connection.execute, "BEGIN")
                yield momoko.Op(connection.execute, stmt, (email, hashed_passwd,
                    name, "dealer", can_sell_comp, is_active, current_user))
                yield momoko.Op(connection.execute, "COMMIT")
                # TODO: send email to user with generated password
                self.set_cookie_name("newdealersaved", str(time.time()))
                self.redirect(u"/dealers/")
        except Exception as e:
            if connection:
                yield momoko.Op(connection.execute, "ROLLBACK")
            mylogger.error(e)
            self.render("error.html", **{})
        else: # si no entro a ninguna excepcion
            # save passwd in log temporary, change !!!!!!!!!!!!!!!!!!!
            mylogger.info("Credenciales new dealer - email: {0} , passwd: {1}".format(email,temp_passwd))

class DealerRechargeQrHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        created_by = self.get_current_user().strip('"')
        dealer = self.get_argument("dealer")
        numqrs = self.get_argument("numqrs")

        try:
            numqrs = int(numqrs)
        except ValueError:
            # front-end size interpret this as error
            self.write(simplejson.dumps([1]))
            self.set_header("Content-Type", "application/json")
            self.finish()
        try:
            connection = yield momoko.Op(self.db.getconn)
            with self.db.manage(connection):
                yield momoko.Op(connection.execute, "BEGIN")
                for _ in range(numqrs):
                    _uuid = qrgen.generate()
                    cursor = yield momoko.Op(self.db.execute,
                                             "INSERT INTO uuid_store (qr_uuid, user_id, \
                                              created_by, created_on) values (%s, %s, %s,\
                                              NOW())", (_uuid, dealer, created_by))
                yield momoko.Op(connection.execute, "COMMIT")
        except Except as e:
            if connection:
                yield momoko.Op(connection.execute, "ROLLBACK")
            mylogger.error(e)
            self.render("error.html", **{})
        else:
            # pack all images up and send them by mail
            self.write(simplejson.dumps([0]))
            self.set_header("Content-Type", "application/json")

class LicensesHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user where email = '%s'" % (email,))
            user_array = cursor_user.fetchone()
            cursor_user.close()
            rol, user_name = '',''
            if not user_array:
                 self.redirect(u"/auth/login/")
                 return
            else:
                rol = user_array[0]
                user_name = user_array[1]
            if rol == '':
                self.clear_current_user()
                self.redirect(u"/auth/login/")
            else:
                self.render("licenses.html", **dict(user_name=user_name,
                                                     email=email,
                                                     rol=rol))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})
