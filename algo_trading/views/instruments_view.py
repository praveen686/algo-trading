from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class InstrumentAddView(generic.edit.FormView):
  template_name = 'instruments/add.html'
  success_url =
  http_method_names = ['post', 'put', 'patch']
