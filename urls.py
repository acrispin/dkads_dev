from tornado.web import StaticFileHandler
from settings import settings
from handlers.home import MainHandler
from handlers.scan import ScanHandler
from handlers.go import GoHandler, SaveEventHandler
from handlers.item import NewItemHandler
from handlers.dashboard import DashBoardHandler, QrRegisteredHandler, SearchQrRegisteredHandler
from handlers.dashboardglobal import GlobalQrHandler, GlobalQrRegisteredHandler, GlobalSearchQrRegisteredHandler
from handlers.login import AuthLoginHandler, AuthLogoutHandler
from handlers.staff import DealerHandler, NewDealerHandler, LicensesHandler, DealerRechargeQrHandler
from handlers.company import CompanyHandler, NewCompanyHandler, SaleQrsHandler, SearchCompanyHandler, CompanyLicensesHandler, CompanyQrsHandler, CompanyLicensesSearchHandler
from handlers.ajaxmethods import SearchUuidHandler, LoadUuidHandler, VerifyUniqueFieldHandler

url_patterns = [
    (r'/$', MainHandler),
    (r'/unidad/([^/]+)', ScanHandler),
    (r'/go/([^/]+)', GoHandler),
    (r'/ep/', SaveEventHandler),
    (r'/registro/$', NewItemHandler),
    (r'/dashboard/$', DashBoardHandler),
    (r'/qrs/registered/$', QrRegisteredHandler),
    (r'/qrs/search/$', SearchQrRegisteredHandler),
    (r'/global/$', GlobalQrHandler),
    (r'/global/qrs/$', GlobalQrRegisteredHandler),
    (r'/global/qrs/search/$', GlobalSearchQrRegisteredHandler),
    (r'/auth/login/$', AuthLoginHandler),
    (r'/auth/logout/', AuthLogoutHandler),
    (r'/dealers/', DealerHandler),
    (r'/dealers/new/', NewDealerHandler),
    (r'/dealers/recharge/', DealerRechargeQrHandler),
    (r'/companies/', CompanyHandler),
    (r'/companies/new/', NewCompanyHandler),
    (r'/companies/sale/', SaleQrsHandler),
    (r'/companies/search/', SearchCompanyHandler),
    (r'/companies/licenses/', CompanyLicensesHandler),
    (r'/companies/licenses/search/', CompanyLicensesSearchHandler),
    (r'/companies/qrs/', CompanyQrsHandler),
    (r'/search/uuid/$', SearchUuidHandler),
    (r'/load/uuid/$', LoadUuidHandler),
    (r'/verify/unique/$', VerifyUniqueFieldHandler),
    # NOTE: I removed relative paths from the templates. Careful with
    # changing these
    (r'/static/(.*)$', StaticFileHandler, dict(path=settings['static_path'])),
    (r'/js/(.*)$', StaticFileHandler, dict(path=settings['static_path'] + '/js')),
    (r'/css/(.*)$', StaticFileHandler, dict(path=settings['static_path'] +'/css')),
    (r'/fonts/(.*)$', StaticFileHandler, dict(path=settings['static_path'] +'/fonts')),
]
