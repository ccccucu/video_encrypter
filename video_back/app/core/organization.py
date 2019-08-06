import easyapi
import app.dao as dao


class OrganizationController(easyapi.BaseController):
    __dao__ = dao.OrganizationDao


class DistributeVideoController(easyapi.BaseController):
    __dao__ = dao.DistributeVideoDao
