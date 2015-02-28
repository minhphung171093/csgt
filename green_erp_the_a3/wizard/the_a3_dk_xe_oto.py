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
    }
    
    _defaults = {
        'tu_ngay': time.strftime('%Y-%m-01'),
        'den_ngay': lambda *a: str(datetime.now() + relativedelta(months=+1, day=1, days=-1))[:10]
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

