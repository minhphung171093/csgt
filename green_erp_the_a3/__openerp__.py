# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'GreenERP The A3',
    'version': '1.1',
    'category': 'GreenERP',
    "author" : "nguyentoanit@gmail.com",
    "website" : "http://vietsolutionis.com/",
    'images': [],
    'depends': ['green_erp_csgt_base','properties','report_aeroo','report_aeroo_ooo'],
    'data': [
             'security/green_erp_the_a3_security.xml',
             'security/ir.model.access.csv',
             'report/thea3_report.xml',
             'report/the_a3_dk_xe_oto_report.xml',
             'wizard/the_a3_dk_xe_oto_view.xml',
             'thea3_view.xml',
             'properties_data.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
