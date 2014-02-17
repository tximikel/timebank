from report.models import Transf_balance_check, Serv_transferences
#from report.models import Report
from serv.models import Service
#from anyapp.models import AnyModel
from model_report.report import reports, ReportAdmin
from model_report.utils import (usd_format, avg_column, sum_column, count_column)
from django.utils.translation import ugettext_lazy as _

class ServiceReport(ReportAdmin):
    title = 'Service Report'
    #title = _('Service Report Name')
    model = Service
    fields = [
        'id',  'description'
    ]
    list_order_by = ('description',)
    #type = 'chart'
    type = 'report'
        
def area_id_label(report, field):
    return _('Area id')
    
def hours_format(value, instance):
    return _(u'%0.2f' % value)

class Report_trf_bal_chk(ReportAdmin):
    title = _('Transferences balance check report')
    model = Transf_balance_check
    fields = [
        'area',  'area_name',  'user_id',  'user_name', 'user__first_name', 'transf_payee',  'transf_debtor',  'balance_tot',  'balance_check', 
    ]
    list_order_by = ('area_name', 'user_name', )
    list_group_by = ('area', )
    list_filter = ('area', )
    #list_filter = ('area', 'user', )
    group_totals = {
        'area': count_column,
        'transf_payee': sum_column,
        'transf_debtor': sum_column,
        'balance_tot': sum_column,
        'balance_check': sum_column
    }
    report_totals = {
        'area': count_column,
        'transf_payee': sum_column,
        'transf_debtor': sum_column,
        'balance_tot': sum_column,
        'balance_check': sum_column
    }
    override_field_labels = {
        'area': area_id_label,
    }
    override_field_formats = {
        'transf_payee': hours_format,
        'transf_debtor': hours_format,
        'balance_tot': hours_format,
        'balance_check': hours_format
    }
    #type = 'chart'        
    type = 'report'
    
def substr_format(value, instance):
    return value[0:50]
    
def bool_format(value, instance):
    if value: 
        bool_value = _('True') 
    else: 
        bool_value = _("False")
    return bool_value

class Report_srv_trf(ReportAdmin):
    title = _('Service transferences report')
    model = Serv_transferences
    fields = [
        'area', 'area_name', 'user_id', 'user_name', 'user__first_name', 'serv_id', 'serv_desc', 'is_offer', 'transf_id', 'transf_user', 'transf_payee', 'transf_payee_sum', 'transf_debtor', 'transf_debtor_sum', 'transf_status', 'transf_request', 'transf_confirm'
    ]
    list_order_by = ('area_name', 'user_name', 'serv_desc', )
    #list_order_by = ('area_name', 'user_name', 'serv_desc', )
    list_group_by = ('area', )
    list_filter = ('area', 'transf_status', 'transf_confirm', )
    #list_filter = ('area', 'user', )
    
    group_totals = {
        'area': count_column,
        'transf_payee': sum_column,
        'transf_payee_sum': sum_column,        
        'transf_debtor': sum_column,
        'transf_debtor_sum': sum_column
    }
    report_totals = {
        'area': count_column,
        'transf_payee': sum_column,
        'transf_payee_sum': sum_column,
        'transf_debtor': sum_column,
        'transf_debtor_sum': sum_column
    }
    override_field_labels = {
        'area': area_id_label,
    }
    override_field_formats = {
        'serv_desc': substr_format,
        'transf_payee': hours_format,
        'transf_payee_sum': hours_format,
        'transf_debtor': hours_format,
        'transf_debtor_sum': hours_format,        
    }
    
    #type = 'chart'        
    type = 'report'

#reports.register('service-report', ServiceReport)
reports.register('transf-balance-check', Report_trf_bal_chk)
reports.register('serv-transferences', Report_srv_trf)
