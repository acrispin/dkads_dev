from tornado import gen, web
import momoko
import simplejson
from handlers.base import BaseHandler
import utils.logginghandler as mylogger

class DashBoardHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            
            #cursor_user = yield momoko.Op(self.db.execute, "select rol,name from sy_user where email = %s" , (email,))
            #http://initd.org/psycopg/docs/usage.html#the-problem-with-the-query-parameters
            sql = 'select rol,name from sy_user where email = %s'
            data = (email,)
            cursor_user = yield momoko.Op(self.db.execute, sql, data)

            #mylogger.debug(cursor_user)
            #mylogger.debug(cursor_user.query) # get the last sql executed

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
                cursor = yield momoko.Op(self.db.execute, "select qr_uuid, is_assigned, user_id, id from uuid_store \
                                                           where is_active and not is_assigned and user_id = %s " , (email,))

                cursor2 = yield momoko.Op(self.db.execute, "select 'today' as criteria ,count(user_id) as hoy \
                                                            from package_store \
                                                            where user_id = %s and is_closed and num_qrs = 1 \
                                                                  and is_active and COALESCE(driver_id,'')<>'' \
                                                                  and DATE(created_on) = DATE(NOW()) \
                                                            union all \
                                                            select 'week' as criteria ,count(user_id) as semana \
                                                            from package_store \
                                                            where user_id = %s and is_closed and num_qrs = 1 \
                                                                  and is_active and COALESCE(driver_id,'')<>'' \
                                                                  and EXTRACT(WEEK FROM created_on) = EXTRACT(WEEK FROM NOW()) \
                                                            union all \
                                                            select 'month' as criteria ,count(user_id) as mes \
                                                            from package_store \
                                                            where user_id = %s and is_closed and num_qrs = 1 \
                                                                  and is_active and COALESCE(driver_id,'')<>'' \
                                                                  and EXTRACT(MONTH FROM created_on) = EXTRACT(MONTH FROM NOW()) " , \
                                                            (email,email,email,))

                if rol == 'staff':
                    sql1 = "select id, TO_CHAR(due_date, 'dd/mm/YYYY'), company_id, driver_id, num_qrs \
                            from package_store \
                            where is_active and user_id = %s \
                            order by due_date asc limit 10"
                elif rol == 'dealer':
                    sql1 = "select ps.id as package_id, TO_CHAR(ps.due_date, 'dd/mm/YYYY') as due_date, ps.driver_id, \
                                   d.name, d.mobile_phone, d.home_phone \
                            from package_store ps \
                            inner join driver d on ps.driver_id = d.dni \
                            where ps.is_active and COALESCE(ps.driver_id,'')<>'' and ps.num_qrs = 1 \
                                  and DATE_PART('day', ps.due_date - NOW()) < 15 \
                                  and ps.user_id = %s \
                            order by ps.due_date asc limit 10"

                cursor3 = yield momoko.Op(self.db.execute, sql1, (email,))

                result = cursor.fetchall()
                cad_json = simplejson.dumps(result) 

                result2 = cursor2.fetchall()
                #mylogger.debug(dict((x, y) for x, y in result2))
                cad_json2 = simplejson.dumps(dict((x, y) for x, y in result2)) 

                result3 = cursor3.fetchall()
                cad_json3 = simplejson.dumps(result3) 

                self.render("dashboard.html", **dict(cad_json=cad_json,
                                                     cad_json2=cad_json2,
                                                     cad_json3=cad_json3,
                                                     user_name=user_name,
                                                     email=email,
                                                     rol=rol))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})       


class QrRegisteredHandler(BaseHandler):
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

            cursor = yield momoko.Op(self.db.execute, " select vd.vehicle_id, vd.driver_id, vd.company_id, \
                                                               vd.package_id, vd.qr_uuid, TO_CHAR(ps.due_date, 'dd/mm/YYYY') as due_date \
                                                        from vehicle_driver vd \
                                                        inner join package_store ps on vd.package_id = ps.id \
                                                        where vd.is_active and ps.is_active \
                                                               and ps.user_id = %s and COALESCE(ps.driver_id,'')<>'' and ps.num_qrs = 1 \
                                                        order by ps.due_date asc" , (email,))
            array_rs = cursor.fetchall()
            columns = [column[0] for column in cursor.description]              
            results = [dict(zip(columns,row)) for row in array_rs]    
            array_json = simplejson.dumps(results) 

            self.render("qrregistered.html", **dict(user_name=user_name,
                                                    email=email,
                                                    rol=rol,
                                                    array_json=array_json))

        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})

    @web.authenticated
    def post(self):
        pass


class SearchQrRegisteredHandler(BaseHandler):
    @gen.coroutine
    def get(self):        
        email = self.get_current_user()
        email = email.strip('"')
        input_search = self.get_argument("input","")
        sql = " select vd.vehicle_id, vd.driver_id, vd.company_id, \
                       vd.package_id, vd.qr_uuid, TO_CHAR(ps.due_date, 'dd/mm/YYYY') as due_date \
                from vehicle_driver vd \
                inner join package_store ps on vd.package_id = ps.id \
                where vd.is_active and ps.is_active \
                       and ps.user_id = %s and COALESCE(ps.driver_id,'')<>'' and ps.num_qrs = 1 \
                       and (lower(vd.vehicle_id) like lower(%s) \
                            or lower(vd.driver_id) like lower(%s) \
                            or lower(vd.qr_uuid::varchar) like lower(%s)) order by ps.due_date asc"
        
        input_search += "%"                  
        params = (email, input_search, input_search, input_search)
        cursor = yield momoko.Op(self.db.execute, sql, params)

        array_rs = cursor.fetchall()
        columns = [column[0] for column in cursor.description]              
        results = [dict(zip(columns,row)) for row in array_rs]       
        self.write(simplejson.dumps(results))
        self.set_header("Content-Type", "application/json")