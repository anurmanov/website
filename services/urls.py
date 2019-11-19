from django.conf.urls import url
from django.views.decorators.cache import never_cache
from services.views import ServicesPageView

urlpatterns = [
    url(r'', never_cache(ServicesPageView.as_view()), name="services"),
]