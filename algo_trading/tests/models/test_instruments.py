from django.test import TestCase

from algo_trading.models import Instrument


class InstrumentsTest(TestCase):
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Instrument.objects.create(symbol="ABC", name="Test Company")

    def test_instrument_token_label(self):
        ins = Instrument.objects.get(id=1)
        field_label = ins._meta.get_field("instrument_token").verbose_name
        self.assertEqual(field_label, "zerodha instrument token")

    def test_get_absolute_url(self):
        author = Instrument.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), "instruments/show/ABC")
