from django.shortcuts import render
from django.views.generic.list import ListView
from services.models import Service
from generic.mixins import CompanyInfoMixin
from visits.generic.count_visitors import count_visitors

class ServicesPageView(ListView, CompanyInfoMixin):
    template_name = 'name_description_list.html'
    model = Service
    @count_visitors
    def get(self, request, *args, **kwargs):
        return super(ServicesPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ServicesPageView, self).get_context_data(**kwargs)
        context['page_title'] = 'Услуги'
        context['list_header'] = 'Наша компания оказывает следующие виды услуг:'
        return context
