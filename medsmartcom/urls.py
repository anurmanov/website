"""medsmartcom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main.views import AdminkaPageView

urlpatterns = [
    path('adminka/', AdminkaPageView.as_view(), name="adminka"),
    path('admin', admin.site.urls),
    url(r'^goods/', include('goods.urls')),
    url(r'^services/', include('services.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^companyinfo/', include('companyinfo.urls')),
    url(r'^visits/', include('visits.urls')),
    url(r'login/', auth_views.LoginView.as_view(template_name = "login.html"), name = "login"),
    url(r'logout/', auth_views.LogoutView.as_view(), name = "logout"),
    url('^$', include('main.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

