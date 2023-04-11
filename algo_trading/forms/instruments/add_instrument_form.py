from django import forms
from ...models.instruments import Instrument


class AddInstrumentForm(forms.Form):
    # These only work when the form is rendered as a table, with these classes being applied to the
    # <th> rows only
    error_css_class = "form-row-error"
    required_css_class = "form-row-required"

    symbol = forms.CharField(
        label="Symbol names",
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Comma separated symbols for import",
                "size": 200,
            }
        ),
    )
