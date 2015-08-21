from tornado import gen, web
import momoko
import os
import time
import uuid
from handlers.base import BaseHandler
import utils.logginghandler as mylogger

IMG_STORE = "static/"

class NewItemHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):        
        try:
            email = self.get_argument("email", "")
            if email == '':
                self.redirect(u"/auth/login/")
            cursor = yield momoko.Op(self.db.execute, "select rol,name from sy_user where email = %s", (email,))
            usuario = cursor.fetchone()
            cursor.close()
            rol = usuario[0]
            user_name = usuario[1]
            if rol == 'staff':
                self.render("newitem.html", **dict(isstaff=True,email=email,user_name=user_name,rol=rol))
            elif rol == 'dealer':
                self.render("newitem.html", **dict(isstaff=False,email=email,user_name=user_name,rol=rol))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})        

    @gen.coroutine
    def post(self):
        connection = None
        try:            
            # get the damn driver's picture
            # http://www.tornadoweb.org/en/stable/httpserver.html#tornado.httpserver.HTTPRequest
            foto_file = self.request.files['condfoto'][0]
            extension = foto_file['content_type'].split("/")[1]
            # NOTE: check filesystem permission when going live
            file_path = os.path.join(IMG_STORE + "%s.%s" % (uuid.uuid1().hex, extension))
            with open(file_path, 'wb') as fd:
                fd.write(foto_file['body'])

            setame = True if self.get_argument("vehsetame", "") else False
            user_email = self.get_argument("user_email")        

            connection = yield momoko.Op(self.db.getconn)
            with self.db.manage(connection):
                yield momoko.Op(connection.execute, "BEGIN")                     
                
                yield momoko.Op(connection.execute, "INSERT INTO driver (dni, \
                                                     name, driver_license, home_phone, mobile_phone, address, path_to_photo, created_on) \
                                                     VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())", \
                                                     (self.get_argument("conddni"), self.get_argument("condnombre"), \
                                                     self.get_argument("condlicencia"), self.get_argument("condtfijo", ""), \
                                                     self.get_argument("condcelular", ""), self.get_argument("conddirec", ""), file_path))
                #raise Exception("Error lanzado luego de registrar el conductor")   
                 
                yield momoko.Op(connection.execute, "INSERT INTO vehicle (plate, \
                                                     mark, model, color, is_setame, created_on) VALUES (%s, %s, %s, %s, %s, NOW())", \
                                                     (self.get_argument("vehplaca"), self.get_argument("vehmarca"), self.get_argument("vehmodelo"), \
                                                     self.get_argument("vehcolor"), setame))                
 
                # crear la licencia individual
                cursor_package = yield momoko.Op(connection.execute, "INSERT INTO package_store (user_id, \
                                                                      num_qrs, due_date, driver_id, is_closed, created_by, created_on) \
                                                                      VALUES(%s, %s, %s, %s, %s, %s, NOW()) \
                                                                      RETURNING id ", \
                                                                      (user_email, 1, self.get_argument("due_date_uni"),\
                                                                      self.get_argument("conddni"), True, user_email)) 
                num_license = cursor_package.fetchone()[0]
                cursor_package.close()

                yield momoko.Op(connection.execute, "INSERT INTO vehicle_driver (vehicle_id, qr_uuid, driver_id, package_id, created_on) \
                                                     VALUES (%s, %s, %s, %s, NOW())", (self.get_argument("vehplaca"), \
                                                     self.get_argument("qruuid"), self.get_argument("conddni"), num_license))
                
                yield momoko.Op(connection.execute, "UPDATE uuid_store SET is_assigned = TRUE, \
                                                     modified_on = NOW() WHERE id = %s", (self.get_argument("numUUID"),))
                
                yield momoko.Op(connection.execute, "COMMIT")      

            self.set_cookie_name("itemsaved",str(time.time()))                
            self.redirect(u"/dashboard/")

        except Exception as e:
            if connection:
                yield momoko.Op(connection.execute, "ROLLBACK")
            #mylogger.error(type(e))
            mylogger.error(e)
            self.render("error.html", **{})          
        
