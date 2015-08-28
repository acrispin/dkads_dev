from tornado import gen
import momoko
import time
from handlers.base import BaseHandler
from utils.functions import qtime
import uuid as ruuid
import utils.logginghandler as mylogger

class GoHandler(BaseHandler):
    @gen.coroutine
    def get(self, goid):
        try:
            # TODO: add scan_event
            cursor_scan_event = yield momoko.Op(self.db.execute, "select id,qr_uuid,latitude,longitude,address, \
                                                                  TO_CHAR(created_on, 'dd/mm/YYYY HH24:MI') \
            													  from scan_event where id = %s", (goid,))
            scan_event = cursor_scan_event.fetchone()
            cursor_scan_event.close()
            if(scan_event):
                uuid = scan_event[1]
                cursor1, cursor2, cursor3 = yield [
                    momoko.Op(self.db.execute, "select c.name, c.driver_license, c.dni, c.path_to_photo, c.home_phone \
                                                from driver c, vehicle_driver \
                                                vc where c.dni = vc.driver_id and \
                                                vc.qr_uuid = %s", (uuid,)),
                    momoko.Op(self.db.execute, "select v.plate, v.is_setame, v.mark, v.model, \
                                                v.color from vehicle v, \
                                                vehicle_driver vc where v.plate \
                                                = vc.vehicle_id and vc.qr_uuid = %s", (uuid,)),
                    momoko.Op(self.db.execute, "select e.ruc, e.description from \
                                                company e, vehicle_driver vc \
                                                where e.ruc = vc.company_id and vc.qr_uuid = %s", (uuid,)),
                    ]
                conductor = cursor1.fetchone()
                vehiculo = cursor2.fetchone()
                empresa = cursor3.fetchone()
                cursor1.close()
                cursor2.close()
                cursor3.close()

                if conductor and vehiculo:
                    if not empresa:
		                self.render("go.html", **dict(desc_empresa=None,
		                                              drivers_name=conductor[0],
		                                              licencia=conductor[1],
		                                              dni=conductor[2],
		                                              # FIXME: image storage
		                                              foto_perfil=conductor[3],
                                                      home_phone=conductor[4],
		                                              auto_plate=vehiculo[0],
		                                              setame=u"S\u00ED" if vehiculo[1] else "No",
		                                              desc_vehiculo=" ".join(vehiculo[2:]),
				                                      address=scan_event[4],
		                                              qtime=scan_event[5],
		                                              timestamp=time.time(),
		                                              uuid=uuid))
                    else:
		                self.render("go.html", **dict(desc_empresa=empresa[1],
		                                              drivers_name=conductor[0],
		                                              licencia=conductor[1],
		                                              dni=conductor[2],
		                                              foto_perfil=conductor[3],
                                                      home_phone=conductor[4],
		                                              auto_plate=vehiculo[0],
		                                              setame=u"S\u00ED" if vehiculo[1] else "No",
		                                              desc_vehiculo=" ".join(vehiculo[2:]),
		                                              address=scan_event[4],
							                          qtime=scan_event[5],
		                                              timestamp=int(time.time()),
		                                              uuid=uuid))
                else:
		            mylogger.error("No conductor ni vehiculo")
            else:
                mylogger.error("No scan_event")
        except Exception as e:
            mylogger.error(e)
            raise


class SaveEventHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        uuid, scan_time, scan_latitude, scan_longitude, scan_address = \
            [self.get_argument(v) for v in ("uuid", "scan_time", "scan_latitude",\
            "scan_longitude", "scan_address")]
        token = ruuid.uuid1().hex.upper()
        yield momoko.Op(self.db.execute, "INSERT INTO scan_event (id, qr_uuid, latitude, longitude, \
             							  address, created_on) VALUES (%s, %s, %s, %s, %s, now())", \
        								  (token, uuid, scan_latitude, scan_longitude, scan_address))
        yield momoko.Op(self.db.execute, "COMMIT")

        taxigo_url = "http://idtaxi.pe/go/%s" % token
        self.render("postevent.html", **dict(taxigo_url=taxigo_url))
