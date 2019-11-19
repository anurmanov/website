from django.conf.urls import url
from django.views.decorators.cache import never_cache
from companyinfo.views import CompanyInfoPageView

urlpatterns = [
    url(r'^$', never_cache(CompanyInfoPageView.as_view()), name='companyinfo'),
]