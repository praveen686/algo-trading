Handling a form

Form.py
---------------
```
from django import forms

class SomeForm(forms.Form):
    name = forms.CharField("Your Name", max_length=100)

    error_css_class = 'my-form-error'
    required_css_class = 'my-form-required' # CSS classes to be used 
```

If using a model to create a form
Form.py
---------------
```
from django.forms import ModelForm
from myapp.models import MyModel


class MyModelForm(ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field5']


    def clean():
        # Additional validations to run on the model form 
        self.field5 = self.field5 / 365 if <condition>
```

View.py
---------------
```
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SomeForm


def view_func_handling_form(request):
    if request.method == 'POST'
      form = SomeForm(request.POST) # bind the form object with the POST request data

      if form.is_valid():
          if 'submit1' in request.POST:
              create_objects_with(form.cleaned_data)

              return HttpResponseRedirect(success_url) # success_url will be the page we want to show if form was successfully processed
          elif 'submit2' in request.POST:
              fetch_from_api(form.cleaned_data)

              return HttpResponseRedirect(data_fetched_success_url) # this URL will be the page we show when data is fetched, maybe just show that data
      else: # invalid form data
          form.add_error('myfield', 'value should be positive and less than module blah blah blah') if 'somefield' in form.errors.keys
          # example to show that we can add errors to specific fields on the form for display when some specific error has happened.

    else: # this creates the empty form on page land.
      form = SomeForm()

    return render(request, template_name.html, { 'form': form })
    # if form was invalid, form.error_messages is populated with field and their errors and the template is
    # rendered with this updated & bound form, with previously entered data & their validation errors from the backend.
    # rendering it with just {{ form }} will display all errors.
    # rendering it manually will need to iterate over all error messages and show them by hand
```



Template.html
----------------

```
<form action="view_func_handling_form" method="post">
  {% csrf_token }
  {{ form }}
  <input type="submit" value="Submit" name="submit1" />
  <input type="submit" value="FetchData" name="submit2" />
</form>
```


{{ form }} can also be the following:
  
{{ form.as_div }}
{{ form.as_table }} # provide surrounding <table> tags in template
{{ form.as_p }}
{{ form.as_ul }} # provide surrounding <ul> tags in template



Printing a dict
------------------

```
import pprint

pprint.pprint(non-nested-dict)

# nested dict
import json

pretty = json.dumps(nested-dict, indent=4)
print(pretty)
```
