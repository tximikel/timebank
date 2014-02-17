from django.db import models
from django.utils.translation import ugettext_lazy as _
from serv.models import Area,  OFFER_CHOICES, TRANSFER_STATUS
from user.models import Profile
from django.contrib.auth.models import User

class Report(models.Model):
    '''
    This class stores information about Reports
    '''
    
    class Meta:
        managed = False

class Transf_balance_check(models.Model):
    #This class stores information about Report of vw_transf_balance_check SQL View
    
    id = models.AutoField(primary_key=True, db_column='user_id', editable=False)
    area_id = models.IntegerField(_(u"Area id"))
    area_name = models.CharField(_(u"Area name"), max_length=40)
    user_id = models.IntegerField(_(u"User id"))
    user_name = models.CharField(_(u"User name"), max_length=30)
    
    '''
    transf_payee = models.DecimalField(_(u"Transference payee"), max_digits=8, decimal_places=2)
    transf_debtor = models.DecimalField(_(u"Transference debtor"), max_digits=8, decimal_places=2)
    balance_tot = models.DecimalField(_(u"Balance total"), max_digits=8, decimal_places=2)
    balance_check = models.DecimalField(_(u"Balance check"), max_digits=8, decimal_places=2)
    '''    
    transf_payee = models.FloatField(_(u"Transference payee"))
    transf_debtor = models.FloatField(_(u"Transference debtor"))
    balance_tot = models.FloatField(_(u"Balance total"))
    balance_check = models.FloatField(_(u"Balance check"))

    area = models.ForeignKey(Area, verbose_name=_("Area"),  null=True, blank=True)
    #user = models.ForeignKey(Profile, verbose_name=_("User"),  null=True, blank=True) 
    user = models.ForeignKey(User, verbose_name=_("User"),  null=True, blank=True,  on_delete=models.DO_NOTHING) 
    
    def transf_payee_format(self):
        return "%s h" % self.transf_payee
        
    def delete(self, key):
        pass
    
    class Meta:
        managed = False
        db_table = 'vw_transf_balance_check'
        verbose_name = _(u"Transferences balance check report") 

class Serv_transferences(models.Model):
    #This class stores information about Report of vw_serv_transf SQL View

    id = models.AutoField(primary_key=True, db_column='user_id', editable=False)
    #id = models.AutoField(primary_key=True)
    #id = models.AutoField(primary_key=True,  db_column='id')
    area_id = models.IntegerField(_(u"Area id"))
    area_name = models.CharField(_(u"Area name"), max_length=40)
    user_id = models.IntegerField(_(u"User id"))
    user_name = models.CharField(_(u"User name"), max_length=30)
    serv_id = models.IntegerField(_(u"Service id"))
    serv_desc = models.TextField(_(u"Service name"))
    is_offer = models.BooleanField(_(u"Is offer?"),  choices = OFFER_CHOICES)
    transf_id = models.IntegerField(_(u"Transf. id"))
    transf_user = models.CharField(_(u"Transf. user"), max_length=30)
    transf_status = models.CharField(_(u"Transf. status"), max_length=1,  choices = TRANSFER_STATUS)
    transf_request = models.DateField(_(u"Request date"))
    transf_confirm = models.DateField(_(u"Confirmation date"))
    transf_payee = models.FloatField(_(u"Transference payee"))
    transf_payee_sum = models.FloatField(_(u"Sum. of Transf. payee"))
    transf_debtor = models.FloatField(_(u"Transference debtor"))
    transf_debtor_sum = models.FloatField(_(u"Sum of Transf. debtor"))
    area = models.ForeignKey(Area, verbose_name=_("Area"),  null=True, blank=True)
    #user = models.ForeignKey(Profile, verbose_name=_("User"),  null=True, blank=True) 
    user = models.ForeignKey(User, verbose_name=_("User"),  null=True, blank=True, on_delete=models.DO_NOTHING) 
    
    class Meta:
        managed = False
        db_table = 'vw_serv_transf'
       #ordering = []
        verbose_name = _(u"Service transferences report") 
