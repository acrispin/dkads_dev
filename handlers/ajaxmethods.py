from tornado import gen
import momoko
from handlers.base import BaseHandler
import simplejson

class SearchUuidHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        s = self.get_argument("search")
        cursor = yield momoko.Op(self.db.execute, "SELECT qr_uuid FROM uuid_store WHERE qr_uuid::varchar LIKE '%s%%%%'" % (s,))
        result = cursor.fetchall()
        print(simplejson.dumps(result))
        self.write(simplejson.dumps(result))
        self.set_header("Content-Type", "application/json")

class LoadUuidHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        t = self.get_argument("type")
        rol = self.get_argument("rol")
        email = self.get_argument("email")
        cursor = None
        if rol == 'staff':
            if t == 'p':               
                cursor = yield momoko.Op(self.db.execute, "select us.qr_uuid, us.is_assigned, ps.user_id \
                    									   from uuid_store us inner join package_store ps ON us.package_id = ps.id \
                    									   where not us.is_assigned order by us.created_on desc")
            elif t == 'r':                
                cursor = yield momoko.Op(self.db.execute, "select us.qr_uuid, us.is_assigned, ps.user_id \
                    									   from uuid_store us inner join package_store ps ON us.package_id = ps.id \
                    									   where us.is_assigned and to_char(us.modified_on, 'yyyy-mm-dd') = to_char(NOW(), 'yyyy-mm-dd')\
                    									   order by us.modified_on desc")
        elif rol == 'dealer':
            if t == 'p':
                cursor = yield momoko.Op(self.db.execute, "select us.qr_uuid, us.is_assigned, ps.user_id \
                    									   from uuid_store us inner join package_store ps ON us.package_id = ps.id \
                    									   where not us.is_assigned and ps.user_id = '%s' \
                                                           order by us.created_on desc" % (email,))
            elif t == 'r':
                cursor = yield momoko.Op(self.db.execute, "select us.qr_uuid, us.is_assigned, ps.user_id \
                    									   from uuid_store us inner join package_store ps ON us.package_id = ps.id \
                    									   where us.is_assigned and ps.user_id = '%s' \
                    									   and to_char(us.modified_on, 'yyyy-mm-dd') = to_char(NOW(), 'yyyy-mm-dd') \
                                                           order by us.modified_on desc" % (email,))
            
        result = cursor.fetchall()        
        self.write(simplejson.dumps(result))
        self.set_header("Content-Type", "application/json")

class VerifyUniqueFieldHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        typ = self.get_argument("type")
        value = self.get_argument("value")        
        cursor = None

        if typ == 'ruc':
            cursor = yield momoko.Op(self.db.execute, "select count(*) from company where ruc = %s " , (value,))
        elif typ == 'conddni':
            cursor = yield momoko.Op(self.db.execute, "select count(*) from driver where dni = %s " , (value,))
        elif typ == 'vehplaca':
            cursor = yield momoko.Op(self.db.execute, "select count(*) from vehicle where plate = %s " , (value,))  
        elif typ == 'dealermail':
            cursor = yield momoko.Op(self.db.execute, "select count(*) from sy_user where email = %s " , (value,))  
            
        result = cursor.fetchone()        
        cursor.close()
        self.write(simplejson.dumps(result))
        self.set_header("Content-Type", "application/json")
