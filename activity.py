# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from datetime import datetime

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
    next_action_date = fields.Function(fields.DateTime('Next Action Date',
            format="%H:%M"),
        'get_next_action_fields')
    next_action = fields.Function(fields.Many2One('activity.activity',
            'Next Activity'),
        'get_next_action_fields')

    def get_last_action_date(self, name=None):
        if not self.activities:
            return None
        Activity = Pool().get('activity.activity')
        act = Activity.search([
                ('resource', '=', 'sale.opportunity,%s' % self.id),
                ('state', '=', 'held'),
                ],
            order=[('dtstart', 'desc')], limit=1)
        return act and act[0].dtstart or None

    @classmethod
    def get_next_action_fields(cls, opportunities, names):
        pool = Pool()
        Activity = pool.get('activity.activity')

        today = datetime.now()
        res = dict((n, {}.fromkeys([o.id for o in opportunities]))
            for n in names)
        for opportunity in opportunities:
            if not opportunity.activities:
                continue
            activities = Activity.search([
                    ('resource', '=', 'sale.opportunity,%s' % opportunity.id),
                    ('state', '=', 'planned'),
                    ('dtstart', '>=', today),
                    ],
                order=[('dtstart', 'asc')], limit=1)
            if not activities:
                continue
            if 'next_action_date' in names:
                res['next_action_date'][opportunity.id] = activities[0].dtstart
            if 'next_action' in names:
                res['next_action'][opportunity.id] = activities[0].id
        return res


class Activity:
    __name__ = 'activity.activity'

    @classmethod
    def default_party(cls):
        opportunity_party_id = Transaction().context.get('opportunity_party')
        if opportunity_party_id:
            return opportunity_party_id
        return super(Activity, cls).default_party()

    # TODO: On 3.4 not necessary any more.
    @classmethod
    def default_allowed_contacts(cls):
        pool = Pool()
        Activity = pool.get('activity.activity')
        Party = pool.get('party.party')
        activity = Activity()
        party_id = cls.default_party()
        if party_id:
            activity.party = Party(cls.default_party())
        else:
            activity.party = None
        allowed = activity.on_change_with_allowed_contacts()
        return allowed
