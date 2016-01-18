from django.conf.urls import patterns, include, url
from django.contrib import admin
from crawler.views import launch, crawlingController,runcrawl,updatelog
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CrawlerUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', launch),
    url(r'^crawl', crawlingController),
    url(r'^runcrawl', runcrawl),
    url(r'^updatelog', updatelog)
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
