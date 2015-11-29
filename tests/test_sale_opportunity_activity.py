# This file is part of the sale_opportunity_activity module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SaleOpportunityActivityTestCase(ModuleTestCase):
    'Test Sale Opportunity Activity module'
    module = 'sale_opportunity_activity'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SaleOpportunityActivityTestCase))
    return suite
