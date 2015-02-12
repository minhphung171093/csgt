# -*- coding: utf-8 -*-
##############################################################################
#
#    HLVSolution, Open Source Management Solution
#
##############################################################################
import time
from openerp.report import report_sxw
from openerp import pooler
from openerp.osv import osv
from openerp.tools.translate import _
import random
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# from green_erp_pharma_report.report import amount_to_text_vn
class Parser(report_sxw.rml_parse):
        
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        pool = pooler.get_pool(self.cr.dbname)
        self.context = context
        self.localcontext.update({
            'get_the_a3':self.get_the_a3,
            'get_line': self.get_line,
            'get_hslq': self.get_hslq,
        })
    
    def get_the_a3(self):
        return self.pool.get('ho.so').browse(self.cr, self.uid, self.context.get('active_ids'))
    
    def get_hslq(self,o):
        hslq_ids = [row.id for row in o.lien_quan_ids]
        hslq = ''
        for line in self.pool.get('ho.so').browse(self.cr, self.uid, hslq_ids):
            hslq += line.name+', '
        if hslq:
            hslq = hslq[:-3]
        return hslq
    
    def get_line(self,line,o):
        count = 0
        subtotal =0
        res =[]
        line_limit = 12
        for data in line:
            count += 1
            res.append({
                            'name': data.name,
                            'nam_sinh': data.nam_sinh,
                            'danh_ban_so': data.danh_ban_so,
                            'hinh_thuc': data.hinh_thuc,
                            })
        if line_limit and line_limit > count:
            while(line_limit != count):
                res.append({
                            'name': ' ',
                            'nam_sinh': ' ',
                            'danh_ban_so': ' ',
                            'hinh_thuc': ' ',
                            })
                count +=1
        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
