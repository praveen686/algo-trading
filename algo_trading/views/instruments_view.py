from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone

class InstrumentAddView(View):
    template_name = 'instruments/add.html'
    success_url = 'instruments/show.html'
    http_method_names = ['post', 'put', 'patch']
    form_class  = Alpha


    # Used to show an empty form for user to add an instrument
    def get(self, request, *args, **kwargs):
        view = NewInstrumentAddView.as_view()
        return view(request, *args, **kwargs)

    # Used to submit the instrument add form to register the new instrument in our DB
    def post(self, request, *args, **kwargs):
        view = InstrumentAddFormView.as_view()
        return view(request, *args, **kwargs)
