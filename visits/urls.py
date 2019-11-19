from django.conf.urls import url
from django.views.decorators.cache import never_cache
from visits.views import visits_json_view, VisitStatisticsView, country_iso_codes, statistic_pages, get_captcha, feedback

urlpatterns = [
    url(r'^get_captcha$', never_cache(get_captcha), name="get_captcha"),
    url(r'^statistic_pages$', never_cache(statistic_pages), name="statistic_pages"),
    url(r'^country_iso_codes$', never_cache(country_iso_codes), name="country_iso_codes"),
    url(r'^json', never_cache(visits_json_view), name="json"),
    url(r'^feedback', never_cache(feedback), name="feedback"),
    url('', never_cache(VisitStatisticsView.as_view()), name="visits"),
]