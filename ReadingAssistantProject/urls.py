"""ReadingAssistantProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ReadingAssistant import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^map/$', views.map),
    # url(r'^map/type=(.*)&entid=(.*)/$', views.entity_modal),
    # url(r'^map/search/type=(.*)&entid=(.*)/$', views.entity_modal),
    url(r'^map/modal/$', views.entity_modal),
    url(r'^map/search/condition=(.*)', views.searchCondition),
    url(r'^generatepoem/$', views.generate_poem_empty),
    url(r'^analysis/$', views.analysis_empty),
    url(r'^rankmodel/$', views.rank_model),
    url(r'^generatepoem/string=(.*)&num=(.*)&type=(.*)&yayuntype=(.*)/$', views.generate_poem),
    url(r'^hello/$', views.hello),
    url(r'^demo/$', views.demo),
    url(r'^test/$', views.test),
    url(r'^', views.homePage),
]
