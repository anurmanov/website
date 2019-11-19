from django.shortcuts import render
from django.views.generic.base import TemplateView
from companyinfo.models import CompanyInfo
from generic.mixins import CompanyInfoMixin
from visits.generic.count_visitors import count_visitors

class ContactsPageView(TemplateView, CompanyInfoMixin):
    template_name = 'contacts.html'
    @count_visitors
    def get(self, request, *args, **kwargs):
        return super(ContactsPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        companyInfo = CompanyInfo.objects.exclude(code = 'about')
        context['companyInfo'] = companyInfo
        return context
