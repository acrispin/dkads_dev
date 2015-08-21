from tornado import gen, web
import momoko
import os
import time
import uuid
import simplejson
from handlers.base import BaseHandler
import utils.logginghandler as mylogger
from utils.functions import getDictJsonFromCursor

IMG_STORE = "static/"

class CompanyHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user \
                                                            where email = %s " , (email,))
            user_array = cursor_user.fetchone()
            cursor_user.close()
            rol, user_name = '',''
            if user_array:
                rol = user_array[0]
                user_name = user_array[1]
            else:
                self.redirect(u"/auth/login/")
                return

            # condicion adicionada para restringir el acceso a otros usuarios que no tengan el rol de staff
            if rol != "staff":
                self.redirect(u"/auth/login/")
                return

            cursor = yield momoko.Op(self.db.execute, "SELECT ruc, description \
                                                       FROM company WHERE is_active")
            companies = cursor.fetchall()
            self.render("company.html", **dict(user_name=user_name,
                                               email=email,
                                               rol=rol,
                                               companies=companies))

        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})

    @web.authenticated
    def post(self):
        pass

class NewCompanyHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user where email = %s " , (email,))
            user_array = cursor_user.fetchone()
            cursor_user.close()
            rol, user_name = '',''
            if user_array:
                rol = user_array[0]
                user_name = user_array[1]
            else:
                self.redirect(u"/auth/login/")
                return

            # condicion adicionada para restringir el acceso a otros usuarios que no tengan el rol de staff
            if rol != "staff":
                self.redirect(u"/auth/login/")
                return

            self.render("newcompany.html", **dict(user_name=user_name,
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
            ruc, compdesc, compadd, compphone, compcontact, email, website = \
            [self.get_argument(v, "") for v in ("ruc", "compdescription", \
            "compaddress","compphone", "compcontactname", "compcorreo", "compweb")]

            is_active = True if self.get_argument("fieldactive", "") else False

            current_user = self.get_current_user()
            stmt = "INSERT INTO company (ruc, description, address, phone, contact_name,\
                    email, website, is_active, created_by, created_on) \
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
       
            connection = yield momoko.Op(self.db.getconn)
            with self.db.manage(connection):
                yield momoko.Op(connection.execute, "BEGIN")
                yield momoko.Op(connection.execute, stmt, (ruc, compdesc, \
                    compadd, compphone, compcontact, email, website, is_active, current_user))
                yield momoko.Op(connection.execute, "COMMIT")                
        except Exception as e:
            if connection:
                yield momoko.Op(connection.execute, "ROLLBACK")
            mylogger.error(e)
            self.render("error.html", **{})
        else:
            self.set_cookie_name("newcompanysaved", str(time.time()))
            self.redirect(u"/companies/")


class SaleQrsHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        email = self.get_current_user()
        email = email.strip('"')
        ruc = self.get_argument("ruc")
        period = self.get_argument("period")        
        numqrs = self.get_argument("numqrs")        

        cursor = yield momoko.Op(self.db.execute, "select fn_SaleQrsToCompany(%s,%s,%s,%s); " , (ruc,period,numqrs,email))       
            
        result = cursor.fetchone()        
        cursor.close()
        self.write(simplejson.dumps(result))
        self.set_header("Content-Type", "application/json")


class SearchCompanyHandler(BaseHandler):
    @gen.coroutine
    def get(self):        
        ruc = self.get_argument("ruc","")
        name = self.get_argument("name","")     
        sql = "SELECT ruc, description FROM company WHERE is_active"
        if ruc:
            ruc += "%"
            sql += " AND ruc LIKE %s"
        if name:
            name += "%"
            sql += (" OR " if ruc else " AND ") + "description LIKE %s" 
        params = (ruc, name)
        cursor = yield momoko.Op(self.db.execute, sql, params)

        companies = cursor.fetchall()
        columns = [column[0] for column in cursor.description]              
        results = [dict(zip(columns,row)) for row in companies]       
        self.write(simplejson.dumps(results))
        self.set_header("Content-Type", "application/json")


class CompanyLicensesHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user \
                                                            where email = %s " , (email,))
            user_array = cursor_user.fetchone()
            cursor_user.close()
            rol, user_name = '',''
            if user_array:
                rol = user_array[0]
                user_name = user_array[1]
            else:
                self.redirect(u"/auth/login/")
                return

            ruc = self.get_argument("ruc", "")
            companyname = self.get_argument("companyname", "")

            cursor = yield momoko.Op(self.db.execute, "select ps.id as license_number, ps.num_qrs as qrs_assigned, \
                                                               (select count(*) from vehicle_driver vd where vd.package_id = ps.id ) as qrs_used, \
                                                               TO_CHAR(ps.due_date, 'dd/mm/YYYY') as due_date, \
                                                               case ps.is_closed when true then 'Cerrado' else 'Abierto' end as closed_status \
                                                        from package_store ps \
                                                        where ps.is_active and ps.user_id = %s \
                                                        and ps.company_id = %s \
                                                        order by ps.due_date asc" , (email, ruc,))
            array_rs = cursor.fetchall()
            columns = [column[0] for column in cursor.description]              
            results = [dict(zip(columns,row)) for row in array_rs]    
            array_json = simplejson.dumps(results)     

            self.render("companylicenses.html", **dict(user_name=user_name,
                                                       email=email,
                                                       rol=rol,
                                                       ruc=ruc,
                                                       companyname=companyname,
                                                       array_json=array_json))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})


class CompanyLicensesSearchHandler(BaseHandler):
    @gen.coroutine
    def get(self):        
        email = self.get_current_user()
        email = email.strip('"')
        input_search = self.get_argument("input","")
        ruc = self.get_argument("ruc","")

        sql = " select ps.id as license_number, ps.num_qrs as qrs_assigned, \
                       (select count(*) from vehicle_driver vd where vd.package_id = ps.id ) as qrs_used, \
                       TO_CHAR(ps.due_date, 'dd/mm/YYYY') as due_date, \
                       case ps.is_closed when true then 'Cerrado' else 'Abierto' end as closed_status \
                from package_store ps \
                where ps.is_active and ps.user_id = %s and ps.company_id = %s"

        if input_search:
            params = (email, ruc, input_search,)
            sql += " and ps.id = %s "
        else:
            params = (email, ruc,)

        sql += " order by ps.due_date asc"

        cursor = yield momoko.Op(self.db.execute, sql, params)

        array_rs = cursor.fetchall()
        columns = [column[0] for column in cursor.description]              
        results = [dict(zip(columns,row)) for row in array_rs]       
        self.write(simplejson.dumps(results))
        self.set_header("Content-Type", "application/json")                        


class CompanyQrsHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user \
                                                            where email = %s " , (email,))
            user_array = cursor_user.fetchone()
            cursor_user.close()
            rol, user_name = '',''
            if user_array:
                rol = user_array[0]
                user_name = user_array[1]
            else:
                self.redirect(u"/auth/login/")
                return

            ruc = self.get_argument("ruc", "")
            companyname = self.get_argument("companyname", "")
            license = self.get_argument("license", "")

            cursor_available = yield momoko.Op(self.db.execute, "select us.id as qr_number, us.qr_uuid \
                                                                 from uuid_store us \
                                                                 where not us.is_assigned and is_active and us.package_id = %s" , (license,))

            cursor_registered = yield momoko.Op(self.db.execute, "select vd.qr_uuid, vd.vehicle_id as placa, vd.driver_id as dni \
                                                                  from vehicle_driver vd \
                                                                  where is_active and vd.package_id = %s" , (license,))

            json_available = getDictJsonFromCursor(cursor_available)
            json_registered = getDictJsonFromCursor(cursor_registered)
            cursor_available.close()
            cursor_registered.close()

            self.render("companyqrs.html", **dict(user_name=user_name,
                                                  email=email,
                                                  rol=rol,
                                                  ruc=ruc,
                                                  companyname=companyname,
                                                  license=license,
                                                  json_available=json_available,
                                                  json_registered=json_registered))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})

    @gen.coroutine
    def post(self):
        connection = None
        try:            
            hdnqrnumber, hdnqruuid, hdnNumberQrsAvailable, hdncompanyname, hdnruc, hdnlicense = \
            [self.get_argument(v, "") for v in ("hdnqrnumber", "hdnqruuid", "hdnNumberQrsAvailable", \
            "hdncompanyname","hdnruc", "hdnlicense")]

            foto_file = self.request.files['condfoto'][0]
            extension = foto_file['content_type'].split("/")[1]
            file_path = os.path.join(IMG_STORE + "%s.%s" % (uuid.uuid1().hex, extension))
            with open(file_path, 'wb') as fd:
                fd.write(foto_file['body'])

            setame = True if self.get_argument("vehsetame", "") else False

            user_email = self.get_current_user()
            user_email = user_email.strip('"')    

            connection = yield momoko.Op(self.db.getconn)
            with self.db.manage(connection):
                yield momoko.Op(connection.execute, "BEGIN")                     
                
                yield momoko.Op(connection.execute, "INSERT INTO driver (dni, \
                                                     name, driver_license, home_phone, mobile_phone, address, path_to_photo, created_on) \
                                                     VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())", \
                                                     (self.get_argument("conddni"), self.get_argument("condnombre"), \
                                                     self.get_argument("condlicencia"), self.get_argument("condtfijo", ""), \
                                                     self.get_argument("condcelular", ""), self.get_argument("conddirec", ""), file_path))
                 
                yield momoko.Op(connection.execute, "INSERT INTO vehicle (plate, \
                                                     mark, model, color, is_setame, created_on) VALUES (%s, %s, %s, %s, %s, NOW())", \
                                                     (self.get_argument("vehplaca"), self.get_argument("vehmarca"), self.get_argument("vehmodelo"), \
                                                     self.get_argument("vehcolor"), setame)) 
               
                yield momoko.Op(connection.execute, "INSERT INTO vehicle_driver (vehicle_id, qr_uuid, driver_id, package_id, created_on) \
                                                     VALUES (%s, %s, %s, %s, NOW())", (self.get_argument("vehplaca"), \
                                                     hdnqruuid, self.get_argument("conddni"), hdnlicense))
                
                yield momoko.Op(connection.execute, "UPDATE uuid_store SET is_assigned = TRUE, \
                                                     modified_on = NOW() WHERE id = %s", (hdnqrnumber,))

                if hdnNumberQrsAvailable == "1": # si solo queda un qr disponible, se debe cambiar el estado de la licencia a cerrado
                    yield momoko.Op(connection.execute, "UPDATE package_store SET is_closed = TRUE, \
                                                         modified_on = NOW() WHERE id = %s", (hdnlicense,))
                
                yield momoko.Op(connection.execute, "COMMIT")      

            self.set_cookie_name("qrsavedbycompany",str(time.time()))                
            self.redirect(u"/companies/qrs/?license={0}&ruc={1}&companyname={2}".format(hdnlicense,hdnruc,hdncompanyname))

        except Exception as e:
            if connection:
                yield momoko.Op(connection.execute, "ROLLBACK")
            mylogger.error(e)
            self.render("error.html", **{})          

