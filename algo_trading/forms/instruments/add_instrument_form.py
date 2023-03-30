from django.forms import ModelForm
from ...models import Instrument


class AddInstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['symbol',]

        error_css_class = 'form-error'
        required_css_class = 'form-required-field'
