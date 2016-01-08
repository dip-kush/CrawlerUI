from django.conf.urls import patterns, include, url
from django.contrib import admin
from crawler.views import launch
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CrawlerUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', launch),
)
