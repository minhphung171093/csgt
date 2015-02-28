# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from datetime import datetime
import datetime
import base64
import calendar
import xlrd
from xlrd import open_workbook,xldate_as_tuple

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
class cap_nhat_oto(osv.osv):
    _name = 'cap.nhat.oto'
    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'hr_identities_attachment.location')
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            if location and attach.store_fname:
                result[attach.id] = self._file_read(cr, uid, location, attach.store_fname, bin_size)
            else:
                result[attach.id] = attach.db_datas
        return result

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        # We dont handle setting data to null
        if not value:
            return True
        if context is None:
            context = {}
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'hr_identities_attachment.location')
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(cr, uid, id, context=context)
            if attach.store_fname:
                self._file_delete(cr, uid, location, attach.store_fname)
            fname = self._file_write(cr, uid, location, value)
            # SUPERUSER_ID as probably don't have write access, trigger during create
            super(cap_nhat_oto, self).write(cr, SUPERUSER_ID, [id], {'store_fname': fname, 'file_size': file_size}, context=context)
        else:
            super(cap_nhat_oto, self).write(cr, SUPERUSER_ID, [id], {'db_datas': value, 'file_size': file_size}, context=context)
        return True

    _columns = {
        'name': fields.date('Cập Nhật Ngày', required=True,states={'done': [('readonly', True)]}),
        'datas_fname': fields.char('File Name',size=256),
        'datas': fields.function(_data_get, fnct_inv=_data_set, string='Data Employee', type="binary", nodrop=True,states={'done': [('readonly', True)]}),
        'store_fname': fields.char('Stored Filename', size=256),
        'db_datas': fields.binary('Database Data'),
        'file_size': fields.integer('File Size'),
        'state':fields.selection([('draft', 'Mới'),('done', 'Đã Cập Nhật')],'Status', readonly=True)
    }
    
    _defaults = {
        'state':'draft',
        'name': time.strftime('%Y-%m-%d'),
                }
    
    def cap_nhat_ho_so(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids[0])
        try:
            recordlist = base64.decodestring(this.datas)
            excel = xlrd.open_workbook(file_contents = recordlist)
            sh = excel.sheet_by_index(0)
        except Exception, e:
            raise osv.except_osv(_('Warning!'), str(e))
        if sh:
            ho_so_obj = self.pool.get('ho.so')
            try:
                dem = 3
                for row in range(3,sh.nrows):
                    name = sh.cell(row, 2).value
                    ngay = sh.cell(row, 1).value
                    if ngay:
                        ngay_dk = ngay[6:10] + '-' + ngay[3:5] + '-'+ ngay[:2]
                        ngay_lap = ngay[6:10] + '-' + ngay[3:5] + '-'+ ngay[:2]
                    else:
                        ngay_dk = False
                        ngay_lap = False
                    ty = ''
                    for col in range(3,sh.ncols):
                        val = sh.cell(row, col).value
                        if val:
                            ty += val+', '
                    if ty:
                        ty = ty[:-2]
                    ho_so_obj.create(cr, uid, {'name':name,'trich_yeu':ty,'ngay_lap':ngay_lap,'ngay_dk':ngay_dk})
                    dem +=1
            except Exception, e:
                raise osv.except_osv(_('Warning!'), str(e)+ ' Line: '+str(dem+1))  
        return self.write(cr, uid, ids, {'state':'done'})
cap_nhat_oto()