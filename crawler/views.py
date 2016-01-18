from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from ExtractDom import initializeParams
from models import Crawl
import json,os
# Create your views here.

def launch(request):
    crawl_list  =[]
    crawl_runs = Crawl.objects.all()[:5]
    for run in crawl_runs:
        crawl_list.append({'id': run.id, 'base_address': run.base_address, 'start_url': run.start_url, 'scope_urls': run.scope_urls})
    return render(request, "index.html", {'crawl_list': crawl_list})


def crawlingController(request):
    crawling_spec = {}
    if request.method == 'POST':
        print request.FILES
        crawling_spec["login_script"] = request.FILES.get('login-script', None)
        crawling_spec["login_url"] = request.POST.get('login-url', "")
        crawling_spec["form_values_script"] = request.FILES.get('form-values-script', None)
        crawling_spec["base_address"] = request.POST.get('base-address', "")
        crawling_spec["start_url"] = request.POST.get('start-url', "")
        crawling_spec["black_list_urls"] = request.POST.get('black-list-urls', "")
        crawling_spec["scope_urls"] = request.POST.get('scope-urls', "")
        crawling_spec["wait_time"] = request.POST.get('wait-time', "")
        print crawling_spec
        print crawling_spec['login_script']
        obj = Crawl(login_script =  crawling_spec["login_script"], login_url = crawling_spec["login_url"] , \
                                    form_values_script = crawling_spec["form_values_script"] , \
                                    base_address =  crawling_spec["base_address"],start_url =  crawling_spec["start_url"], \
                                    black_list_urls =  crawling_spec["black_list_urls"], \
                                    scope_urls =  crawling_spec["scope_urls"], \
                                    wait_time =  crawling_spec["wait_time"])
        #print login_script, login_url, form_values_script, base_address, start_url, black_list_urls, scope_urls, wait_time
        obj.save()
        #initializeParams(crawling_spec)
        return HttpResponse("Do something")


def runcrawl(request):
    print "request"
    crawl_spec_dict = {}
    if request.is_ajax():
        print "request inside"
        if request.method == 'POST':
            id_val = request.POST['id']
            if id_val:
                crawl = Crawl.objects.get(id=id_val)
                print crawl
                crawl_spec_dict = {"login_script": crawl.login_script, "login_url": crawl.login_url, \
                                    "form_values_script": crawl.form_values_script, "base_address": crawl.base_address, \
                                    "start_url": crawl.start_url, "black_list_urls":crawl.black_list_urls, \
                                    "scope_urls":crawl.scope_urls, "wait_time": crawl.wait_time}
                print crawl_spec_dict
                initializeParams(crawl_spec_dict)
                return HttpResponse(json.dumps({'success': 1}))
    return HttpResponse(json.dumps({'success': 0}))


def updatelog(request):
    end_signal = 0
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, 'crawling.log')
    print path
    f = open(path)
    lines =  f.readlines()
    log = ''.join(lines).replace("\n", "|||")
    if log.find("THE END") != -1:
        end_signal = 1
    return HttpResponse(json.dumps({'log': log, 'end': end_signal}))
