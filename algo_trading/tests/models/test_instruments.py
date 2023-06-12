from django.test import TestCase

from algo_trading.models import Instrument


class InstrumentsTest(TestCase):
    def setUpTestData():
        Instrument.objects.create(trading_symbol="ABC", name="Test Company")

    def test_instrument_token_label(self):
        ins = Instrument.objects.get(id=1)
        field_label = ins._meta.get_field("instrument_token").verbose_name
        self.assertEqual(field_label, "zerodha instrument token")

    def test_get_absolute_url(self):
        ins = Instrument.objects.get(id=1)
        self.assertEqual(ins.get_absolute_url(), "/instruments/show/ABC")
