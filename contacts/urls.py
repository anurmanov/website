from django.conf.urls import url
from django.views.decorators.cache import never_cache
from contacts.views import ContactsPageView

urlpatterns = [
    url(r'^$', never_cache(ContactsPageView.as_view()), name='contacts'),
]