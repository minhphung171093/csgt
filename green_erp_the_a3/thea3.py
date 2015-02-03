# -*- coding: utf-8 -*-

import time

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp

class ho_so(osv.osv):
    _name = "ho.so"
    _columns = {
        'name': fields.char('Số hồ sơ', size=20,required = True),
        'ngay_lap': fields.date('Lập ngày'),
        'ngay_dk': fields.date('Đăng ký ngày'),
        'ngay_luu': fields.date('Nộp lưu ngày'),
        'so_luu': fields.char( 'Số lưu trữ',size = 20),
        'trich_yeu': fields.text("Trích yếu"),
        'doi_tuong_line': fields.one2many('doi.tuong','ho_so_dt_id','Đối tượng trong vụ'),
        'lien_quan_ids': fields.many2many(
                    'ho.so',
                    'lien_quan_ids',
                    'name',
                    string="Hồ sơ liên quan"
                                ),

                } 
ho_so()
class doi_tuong(osv.osv):
    _name = "doi.tuong"
    _columns = {
        'name': fields.char('Họ tên', size=30,required = True),
        'nam_sinh': fields.char('Sinh năm',size=4),
        'danh_ban_so': fields.char('Danh bản số',size=10),
        'hinh_thuc': fields.char('Hình thức, mức độ xử lý', size = 50),
        'ho_so_dt_id': fields.many2one('ho.so',"Hồ sơ",ondelete='cascade'),
                }
doi_tuong()
