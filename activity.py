# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction

__metaclass__ = PoolMeta
__all__ = ['Activity', 'SaleOpportunity']


class SaleOpportunity:
    __name__ = 'sale.opportunity'

    activities = fields.One2Many('activity.activity', 'resource',
        'Activities', context={
            'opportunity_party': Eval('party'),
            }, depends=['party'])
    last_action_date = fields.Function(fields.DateTime('Last Action'),
        'get_last_action_date')

    def get_last_action_date(self, name=None):
        if not self.activities:
            return None
        Activity = Pool().get('activity.activity')
        act = Activity.search([
                ('resource', '=', 'sale.opportunity,%s' % self.id)
                ],
            order=[('dtstart', 'desc')], limit=1)
        return act and act[0].dtstart or None


class Activity:
    __name__ = 'activity.activity'

    @classmethod
    def default_party(cls):
        opportunity_party_id = Transaction().context.get('opportunity_party')
        if opportunity_party_id:
            return opportunity_party_id
        return super(Activity, cls).default_party()
