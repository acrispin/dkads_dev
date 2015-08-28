from tornado import gen, web
import momoko
import simplejson
from handlers.base import BaseHandler
import utils.logginghandler as mylogger
from utils.functions import getDictJsonFromCursor

class GlobalQrHandler(BaseHandler):
    @gen.coroutine
    @web.authenticated
    def get(self):
        try:
            email = self.get_current_user()
            email = email.strip('"')
            
            sql = 'select rol,name from sy_user where email = %s'
            data = (email,)
            cursor_user = yield momoko.Op(self.db.execute, sql, data)
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

            sql = " select 'today' as criteria ,count(ps.user_id) as hoy \
                    from package_store ps \
                    inner join sy_user u on ps.user_id = u.email \
                    where ps.is_active and ps.is_closed and ps.num_qrs = 1 and COALESCE(ps.driver_id,'')<>'' \
                          and DATE(ps.created_on) = DATE(NOW()) \
                          and u.rol = 'dealer' \
                    union all \
                    select 'week' as criteria ,count(ps.user_id) as semana \
                    from package_store ps \
                    inner join sy_user u on ps.user_id = u.email \
                    where ps.is_active and ps.is_closed and ps.num_qrs = 1 and COALESCE(ps.driver_id,'')<>'' \
                          and EXTRACT(WEEK FROM ps.created_on) = EXTRACT(WEEK FROM NOW()) \
                          and u.rol = 'dealer' \
                    union all \
                    select 'month' as criteria ,count(ps.user_id) as mes \
                    from package_store ps \
                    inner join sy_user u on ps.user_id = u.email \
                    where ps.is_active and ps.is_closed and ps.num_qrs = 1 and COALESCE(ps.driver_id,'')<>'' \
                          and EXTRACT(MONTH FROM ps.created_on) = EXTRACT(MONTH FROM NOW()) \
                          and u.rol = 'dealer'"

            cursor = yield momoko.Op(self.db.execute, sql)

            result = cursor.fetchall()
            dict_json = simplejson.dumps(dict((x, y) for x, y in result)) 

            self.render("dashboardglobal.html", **dict(dict_json=dict_json,
                                                       user_name=user_name,
                                                       email=email,
                                                       rol=rol))
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})       


class GlobalQrRegisteredHandler(BaseHandler):
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

            sql = " select ps.user_id as email, min(u.name) as name, sum(ps.num_qrs) as total_qrs \
                    from package_store ps \
                    inner join sy_user u on ps.user_id = u.email \
                    where ps.is_active and ps.is_closed \
                          and ps.num_qrs = 1 and COALESCE(ps.driver_id,'')<>'' \
                          and u.rol = 'dealer'"

            sql += " group by ps.user_id "

            cursor = yield momoko.Op(self.db.execute, sql)

            array_json = getDictJsonFromCursor(cursor)
            cursor.close()

            self.render("qrregisteredglobal.html", **dict(user_name=user_name,
                                                    email=email,
                                                    rol=rol,
                                                    array_json=array_json))

        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})

    @web.authenticated
    def post(self):
        pass


class GlobalSearchQrRegisteredHandler(BaseHandler):
    @gen.coroutine
    def get(self):        
        email = self.get_current_user()
        email = email.strip('"')
        input_search = self.get_argument("input","")
        input_period = self.get_argument("period","")

        filter_period = ""
        if input_period == 't':
            filter_period = " and DATE(ps.created_on) = DATE(NOW()) "
        elif input_period == "w":
            filter_period = " and EXTRACT(WEEK FROM ps.created_on) = EXTRACT(WEEK FROM NOW()) "
        elif input_period == "m":
            filter_period = " and EXTRACT(MONTH FROM ps.created_on) = EXTRACT(MONTH FROM NOW()) "

        sql = " select ps.user_id as email, min(u.name) as name, sum(ps.num_qrs) as total_qrs \
                from package_store ps \
                inner join sy_user u on ps.user_id = u.email \
                where ps.is_active and ps.is_closed \
                      and ps.num_qrs = 1 and COALESCE(ps.driver_id,'')<>'' and u.rol = 'dealer' \
                      and (lower(ps.user_id) like lower(%s) or lower(u.name) like lower(%s)) "
        sql += filter_period
        sql += " group by ps.user_id order by name asc "
        
        input_search += "%"                  
        params = (input_search, input_search)
        cursor = yield momoko.Op(self.db.execute, sql, params)      

        array_json = getDictJsonFromCursor(cursor)
        cursor.close()

        self.write(array_json)
        self.set_header("Content-Type", "application/json")