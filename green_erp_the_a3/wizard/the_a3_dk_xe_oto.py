# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class the_a3_dk_xe_oto(osv.osv_memory):
    _name = "the.a3.dk.xe.oto"
    
    _columns = {
            'tu_ngay': fields.date('Từ ngày', required = True),
            'den_ngay': fields.date('Đến ngày', required = True),
            'cb_lap_hs': fields.char('Cán bộ lập hồ sơ', size=1024, required = True),
    }
    
    def _get_cb_lap_hs(self, cr, uid, context=None):
        property_pool = self.pool.get('admin.property')
        default_canbo_lap_hoso = False
        property_obj = property_pool._get_project_property_by_name(cr, uid, 'default_canbo_lap_hoso') or None
        if property_obj:
            default_canbo_lap_hoso = property_obj.value
        return default_canbo_lap_hoso
    
    _defaults = {
        'tu_ngay': time.strftime('%Y-%m-01'),
        'den_ngay': lambda *a: str(datetime.now() + relativedelta(months=+1, day=1, days=-1))[:10],
        'cb_lap_hs': _get_cb_lap_hs,
        }
    
    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'the.a3.dk.xe.oto'
        datas['form'] = self.read(cr, uid, ids)[0]
        datas['form'].update({'active_id':context.get('active_ids',False)})
        return {'type': 'ir.actions.report.xml', 'report_name': 'the_a3_dk_xe_oto_report', 'datas': datas}
        
the_a3_dk_xe_oto()

