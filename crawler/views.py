from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from ExtractDom import initializeParams
from BeautifulSoup import BeautifulSoup
from models import Crawl, Workflow, Link, StartHeader
import networkx as nx
import json,os

# Create your views here.

def launch(request):
    crawl_list  =[]
    crawl_runs = Crawl.objects.all()[:5]
    for run in crawl_runs:
        crawl_list.append({'id': run.id, 'base_address': run.base_address, 'start_url': run.start_url, 'scope_urls': run.scope_urls})
    return render(request, "index.html", {'crawl_list': crawl_list})



def showGraph(request):
    return render(request, "graph.html")



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
        crawling_spec["depth"] = request.POST.get('depth', "100")
        #print crawling_spec
        data = ""
        lines = crawling_spec['login_script'].readlines()
        for line in lines:
            data = data+line.strip()
        bs =  BeautifulSoup(data)
        #print bs.findAll("tr") 
        obj = Crawl(login_script =  crawling_spec["login_script"], login_url = crawling_spec["login_url"] , \
                                    form_values_script = crawling_spec["form_values_script"] , \
                                    base_address =  crawling_spec["base_address"],start_url =  crawling_spec["start_url"], \
                                    black_list_urls =  crawling_spec["black_list_urls"], \
                                    scope_urls =  crawling_spec["scope_urls"], \
                                    wait_time =  crawling_spec["wait_time"], \
                                    depth = crawling_spec["depth"])
        #print login_script, login_url, form_values_script, base_address, start_url, black_list_urls, scope_urls, wait_time
        obj.save()
        crawling_spec["login_script"] = data
        fsm = initializeParams(crawling_spec)
        #print graph
        return HttpResponse("Do something")


def runcrawl(request):
    print "request"
    crawl_spec_dict = {}
    #if request.is_ajax():
        #if request.method == 'POST':
    id_val = 1
    #id_val = request.POST['id']
    if id_val:
        crawl = Crawl.objects.get(id=id_val)
        print crawl
        crawl_spec_dict = {"login_script": crawl.login_script, "login_url": crawl.login_url, \
                            "form_values_script": crawl.form_values_script, "base_address": crawl.base_address, \
                            "start_url": crawl.start_url, "black_list_urls":crawl.black_list_urls, \
                            "scope_urls":crawl.scope_urls, "wait_time": crawl.wait_time, "depth":crawl.depth}
        print crawl_spec_dict
        fsm = initializeParams(crawl_spec_dict)
        print "graph object",fsm.graph.nodes()
        pathSourcetoSink(fsm, crawl, crawl.login_url)
        return HttpResponse(json.dumps({'success': 1}))
    #retur HttpResponse(json.dumps({'success': 0}))


def pathSourcetoSink(fsm,crawl,url):
        graph = fsm.graph
        sink_nodes = [node for node, outdegree in graph.out_degree
                        (graph.nodes()).items() if outdegree == 0]
        source_nodes = [node for node, indegree in graph.in_degree
                        (graph.nodes()).items() if indegree == 0]
        if source_nodes == []:
            source_nodes.append(0)
        wflow_no = 1
        for sink in sink_nodes:
            for source in source_nodes:
                for path in nx.all_simple_paths(graph, source=source, target=sink):
                    print path
                    obj = Workflow(scan_id=crawl,wflow_no = wflow_no) 
                    obj.save()
                    for i in range(len(path)-1):
                        #print path[i]
                        link = graph.edge[path[i]][path[i+1]][0]["event"].xpath
                        header = graph.edge[path[i]][path[i+1]][0]["header"] 
                        wflow = Workflow.objects.get(scan_id=crawl,wflow_no = wflow_no)
                        #print wflow.wflow_no
                        linkobj = Link(wflow_id = wflow, link = link, order_id = i+1,header=header)
                        linkobj.save()
                        print graph.edge[path[i]][path[i+1]][0]["event"].xpath
                    wflow_no+=1    
        start_url_header = fsm.start_header
        login_url_header = fsm.login_header
        headerObj = StartHeader(scan_id=crawl,start_url_header=start_url_header,login_url_header=login_url_header)
        headerObj.save()            
        
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

def readJsonDataFile(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, 'jsonDataFile.txt')
    f = open(path)
    data = ""
    lines =  f.readlines()
    for line in lines:
        data = data+line.strip()
    return HttpResponse(json.dumps({'jsondata': data}))
     


    
