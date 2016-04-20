from django.conf.urls import patterns, include, url
from django.contrib import admin
from crawler.views import launch,error,allLogs,runResult, crawlingController,runcrawl,updatelog,readJsonDataFile,showGraph,getWorkflow
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
    url(r'^updatelog', updatelog),
    url(r'^readJsonDataFile',readJsonDataFile),
    url(r'^graph', showGraph),
    url(r'^getworkflow', getWorkflow),
    url(r'^runresult', runResult),
    url(r'^error', error),
    url(r'^alllog', allLogs)
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
