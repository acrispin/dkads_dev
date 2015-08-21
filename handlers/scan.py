from tornado import gen
import momoko
import time
from handlers.base import BaseHandler
import utils.logginghandler as mylogger
from utils.functions import qtime

class ScanHandler(BaseHandler):
    @gen.coroutine
    def get(self, uuid):
        try:
            # TODO: debieran ademar solo filtrarse los que estan activos
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
                    self.render("info.html", **dict(desc_empresa=None,
                                                    drivers_name=conductor[0],
                                                    licencia=conductor[1],
                                                    dni=conductor[2],
                                                    # FIXME: image storage
                                                    foto_perfil=conductor[3],
                                                    home_phone=conductor[4],
                                                    auto_plate=vehiculo[0],
                                                    setame=u"S\u00ED" if vehiculo[1] else "No",
                                                    desc_vehiculo=" ".join(vehiculo[2:]),
                                                    qtime=qtime(),
                                                    timestamp=time.time(),
                                                    uuid=uuid))
                else:
                    self.render("info.html", **dict(desc_empresa=empresa[1],
                                                    drivers_name=conductor[0],
                                                    licencia=conductor[1],
                                                    dni=conductor[2],
                                                    foto_perfil=conductor[3],
                                                    home_phone=conductor[4],
                                                    auto_plate=vehiculo[0],
                                                    setame=u"S\u00ED" if vehiculo[1] else "No",
                                                    desc_vehiculo=" ".join(vehiculo[2:]),
                                                    qtime=qtime(),
                                                    timestamp=int(time.time()),
                                                    uuid=uuid))
            else:
                #pass
                mylogger.info("no data profile")
        except Exception as e:
            mylogger.error(e)
            self.render("error.html", **{})
            #raise