from django.shortcuts import render
from django.views.generic.base import TemplateView
from companyinfo.models import CompanyInfo
from generic.mixins import CompanyInfoMixin
from visits.generic.count_visitors import count_visitors

class CompanyInfoPageView(TemplateView, CompanyInfoMixin):
    template_name = 'about.html'
    @count_visitors
    def get(self, request, *args, **kwargs):
        return super(CompanyInfoPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cont = super(CompanyInfoPageView, self).get_context_data(**kwargs)
        cont['about'] = CompanyInfo.objects.get(code = 'about')
        return cont
# Create your views here.
