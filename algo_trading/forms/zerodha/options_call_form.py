from django import forms


class OptionsCallForm(forms.Form):
    call_blob = forms.CharField(strip=True)
