from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

__metaclass__ = PoolMeta

__all__ = ['Activity', 'SaleOpportunity']

class Activity:
    __name__ = 'activity.activity'

    opportunity = fields.Many2One('sale.opportunity', 'Oportunity',
        on_change_with=['reference'])


    def on_change_with_opportunity(self):
        print "aaaaaaaaaaaaaaaaaaaaAAA:",self.reference


class SaleOpportunity:
    __name__ = 'sale.opportunity'

    activities = fields.One2Many('activity.activity', 'opportunity',
        'Activities')




