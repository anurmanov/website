from django.views.generic.base import ContextMixin
from companyinfo.models import CompanyInfo

class PageNumberMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(PageNumberMixin, self).get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', 1)
        return context

class CompanyInfoMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        class empty(object):
            pass
        context = super(CompanyInfoMixin, self).get_context_data(**kwargs)
        companyInfoObj = empty()
        setattr(companyInfoObj, 'address', CompanyInfo.objects.get(code = 'jur_address').value)
        setattr(companyInfoObj, 'telephone', CompanyInfo.objects.get(code = 'telephone').value)
        setattr(companyInfoObj, 'email', CompanyInfo.objects.get(code = 'email').value)
        #companyInfoObj.address = CompanyInfo.objects.get(code = 'jur_address')
        #companyInfoObj.telephone = CompanyInfo.objects.get(code = 'telephone')
        #companyInfoObj.email = CompanyInfo.objects.get(code = 'email')
        context['company_info'] = companyInfoObj
        return context