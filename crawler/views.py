from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from ExtractDom import initializeParams
from BeautifulSoup import BeautifulSoup
from lxml import etree
from lxml.html.clean import clean_html
from models import Crawl, Workflow, Link, StartHeader
from response_comparator import htmlcompare
from header import Header
import networkx as nx
import urllib2
import json,os
import requests
# Create your views here.

def launch(request):
    crawl_list  =[]
    crawl_runs = Crawl.objects.all()[:5]
    for run in crawl_runs:
        crawl_list.append({'id': run.id, 'base_address': run.base_address, 'start_url': run.start_url, 'scope_urls': run.scope_urls})
    return render(request, "index.html", {'crawl_list': crawl_list})

def runResult(request):
    return render(request, 'wflow.html')

def allLogs(request):
    end_signal = 0
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, 'crawling.log')
    print path
    f = open(path)
    lines =  f.readlines()
    for line in lines:
        line = line.strip()
    return render(request, "log.html", {"log": lines})



def showGraph(request):
    return render(request, "graph.html")

def error(request):
    pass

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
        #crawling_spec["proxy_address"] = request.POST.get('proxy-address', "")
        #print crawling_spec
        login_data = ""
        form_data = ""
        lines = crawling_spec['login_script'].readlines()
        for line in lines:
            login_data = login_data+line.strip()
        lines = crawling_spec['form_values_script'].readlines()
        for line in lines:
            form_data = form_data+line.strip()

        bs =  BeautifulSoup(form_data)
        print bs
        #print bs.findAll("tr") 
        obj = Crawl(login_script =  crawling_spec["login_script"], login_url = crawling_spec["login_url"] , \
                                    form_values_script = crawling_spec["form_values_script"] , \
                                    base_address =  crawling_spec["base_address"],start_url =  crawling_spec["start_url"], \
                                    black_list_urls =  crawling_spec["black_list_urls"], \
                                    scope_urls =  crawling_spec["scope_urls"], \
                                    wait_time =  crawling_spec["wait_time"], \
                                    depth = crawling_spec["depth"])
                                    #proxy_address = crawling_spec["proxy_address"])
        #print login_script, login_url, form_values_script, base_address, start_url, black_list_urls, scope_urls, wait_time
        obj.save()
        crawling_spec["login_script"] = login_data
        crawling_spec["form_values_script"] = form_data
        fsm = initializeParams(crawling_spec)
        #pathSourcetoSink(fsm, crawl, crawl.login_url)
        #print graph
        if fsm:
            returnJsonGraph(fsm.graph)
            number_of_nodes = fsm.graph.number_of_nodes()
            number_of_edges = len(fsm.graph.edges())
            nodes = getNodes(fsm.graph)
            edges = getEdges(fsm.graph)
            crawl = Crawl.objects.latest("id")
            pathSourcetoSink(fsm, crawl)    
            print crawl.id
            workflows = getWfs(crawl.id)
            print "workflows"
            print workflows
            #print edges
            #print nodes
            return render(request, 'run.html', {'num_nodes': number_of_nodes,'num_edges':number_of_edges, 'nodes': nodes, 'edges': edges, 'workflows': workflows})
        else:
            return render(request, "error.html") 


def getNodes(graph):
    numberofnodes = graph.number_of_nodes()
    node_list = []
    for i in range(numberofnodes):
        node_dict = {}
        node_dict["num"] = i
        node_dict["path"] = printBackTrackPath(graph.node[i]['nodedata'].backtrackPath)
        node_list.append(node_dict)
    return node_list

def printBackTrackPath(path):
    fullpath = ""
    for entity in path:
        fullpath+=str(entity)
        fullpath+=" "
    return fullpath


def getEdges(graph):
    edge_list = []
    edges = graph.edges()
    numEdges = len(edges)
    for i in range(numEdges):       
        edge_dict = {}
        source = edges[i][0]
        dest = edges[i][1]
        edge_dict["edge"] = str(edges[i])
        edge_dict["info"] = str(graph[source][dest])
        edge_list.append(edge_dict)
    return edge_list


def returnJsonGraph(graph):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, 'static/jsonDataFile.txt')
    jsonDataFile = open(path, "w")
    graphData = {}
    graphData["nodes"] = []
    graphData["links"] = []
    numberofnodes = graph.number_of_nodes()
    for i in range(numberofnodes):
        newNodeDict = {}
        newNodeDict["name"] = i
        newNodeDict["group"] = 1
        graphData["nodes"].append(newNodeDict)
    edges = graph.edges()
    numEdges = len(edges)
    for i in range(numEdges):
        source = edges[i][0]
        dest = edges[i][1]
        newLinkDict = {
        "source": source,
        "target": dest,
        "value": 50
        }
        graphData["links"].append(newLinkDict)
    data = json.dumps(graphData)
    jsonDataFile.write(data)
    jsonDataFile.close()
    #print data


def runcrawl(request):
    print "request"
    crawl_spec_dict = {}
    #if request.is_ajax():
    if request.method == 'GET':
    #id_val = 1
        id_val = request.GET['id']
        crawl = Crawl.objects.get(id=id_val)
        print crawl
        crawl_spec_dict = {"login_script": crawl.login_script, "login_url": crawl.login_url, \
                            "form_values_script": crawl.form_values_script, "base_address": crawl.base_address, \
                            "start_url": crawl.start_url, "black_list_urls":crawl.black_list_urls, \
                            "scope_urls":crawl.scope_urls, "wait_time": crawl.wait_time, "depth":crawl.depth } 
                            #"proxy_address": crawl.proxy_address}
        print crawl_spec_dict
        fsm = initializeParams(crawl_spec_dict)
        #print "graph object",fsm.graph.nodes()
        #pathSourcetoSink(fsm, crawl)
        if fsm:
            number_of_nodes = fsm.graph.number_of_nodes()
            number_of_edges = len(fsm.graph.edges())
            nodes = getNodes(fsm.graph)
            edges = getEdges(fsm.graph)
            crawl = Crawl.objects.latest("id")
            #pathSourcetoSink(fsm, crawl)
            print crawl.id
            workflows = getWfs(crawl.id)
            print "workflows"
            print workflows
            #print edges
            #print nodes
            return render(request, 'run.html', {'num_nodes': number_of_nodes,'num_edges':number_of_edges, 'nodes': nodes, 'edges': edges, 'workflows': workflows})
        else:
            return render(request, "error.html")            
        #return HttpResponse(json.dumps({'success': 1}))
#retur HttpResponse(json.dumps({'success': 0}))


def pathSourcetoSink(fsm,crawl):
        graph = fsm.graph
        criticalStates = fsm.criticalStates
        
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
                    critical = False
                    critical_path = False
                    for i in range(len(path)-1):
                        #print path[i]
                        critical = False
                        link = graph.edge[path[i]][path[i+1]][0]["event"].xpath
                        header = graph.edge[path[i]][path[i+1]][0]["header"] 
                        dom = graph.node[path[i+1]]['nodedata'].domString
                        wflow = Workflow.objects.get(scan_id=crawl,wflow_no = wflow_no)
                        if path[i+1] in criticalStates:
                            critical = True
                            critical_path = True        
                        #print wflow.wflow_no
                        linkobj = Link(wflow_id = wflow, link = link, order_id = i+1,header=header, response_dom=dom, critical_node=critical)
                        linkobj.save()
                        print graph.edge[path[i]][path[i+1]][0]["event"].xpath
                    if critical_path==True:
                        obj.critical = True
                        obj.save()
                    wflow_no+=1    
        start_url_header = fsm.start_header
        login_url_header = fsm.login_header
        login_dom = fsm.login_dom
        headerObj = StartHeader(scan_id=crawl,start_url_header=start_url_header,login_url_header=login_url_header, login_dom = login_dom)
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
    
def cleanCode(domString):
    domString = clean_html(domString)
    tree   = etree.HTML(domString.replace('\r', ''))
    domString = '\n'.join([ etree.tostring(stree, pretty_print=True, method="xml")
                          for stree in tree ])
    return domString
 
def getWorkflow(request):    
    vulnerable_wflows= []
    if request.method == "GET":
        id_val = request.GET["id"]
        crawl_obj, vulnerable_wflows, non_vulnerable_wflows = getWorkflows(int(id_val), True)
    print non_vulnerable_wflows
    if vulnerable_wflows:
        return render(request, "wflow.html", {"crawl_obj": crawl_obj, "vwflows": vulnerable_wflows, "nonvflows": non_vulnerable_wflows})
    else:
        return render(request, "wflow.html")        


def executeWorkflows(workflows):
    vulnerable_wflows = []
    for wf_obj,wflow in workflows:
        s = requests.Session()
        print "Executing Workflow", wf_obj.wflow_no
        for order, req in enumerate(wflow):
            flag = False
            if req.critical == False:
                print "Executing Request",order+1 
                if req.method == "GET":
                    r = s.get(req.url, data=req.data)
                elif req.method == "POST":  
                    r = s.post(req.url, data=req.data)
                print htmlcompare(cleanCode(r.text),cleanCode(req.dom))
                print "===================================="
                #print r.text
                print "====================================="
                #print req.dom
                
                             
                if not htmlcompare(cleanCode(r.text),cleanCode(req.dom)):
                    flag = True
                    print "it's correct"
        
        if flag:
            print "No Sequence Violation"
        else:
            wf_obj.vulnerable = True
            wf_obj.save()
            vulnerable_wflows.append((wf_obj, wflow))
            print "Sequence Violation"    

    return vulnerable_wflows   


def getWfs(crawl_id):
    workflows = []
    crawl_obj =  Crawl.objects.get(id=crawl_id)
    startHeader =  StartHeader.objects.get(scan_id=crawl_obj)
    wflows_obj = Workflow.objects.filter(scan_id=crawl_obj)
    return wflows_obj



 
def getWorkflows(crawl_id, critical_bool):
    #crawl_id = 1
    workflows = []
    non_vworkflows = []
    crawl_obj =  Crawl.objects.get(id=crawl_id)
    startHeader =  StartHeader.objects.get(scan_id=crawl_obj)
    wflows_obj = Workflow.objects.filter(scan_id=crawl_obj)
    #non_vflows_obj = Workflow.objects.filter(scan_id=crawl_obj, critical=False)
    #all_wflows = wflows_obj+non_vlows_obj
    print wflows_obj 
    for wf in wflows_obj:
        wflow = []
        print wf.wflow_no
        links = Link.objects.filter(wflow_id=wf).order_by("order_id")
        #links.sort(key=lambda x:x.order_id)
        if startHeader.login_url_header:
            header = headerSplit(startHeader.login_url_header, False, startHeader.login_dom)
            wflow.append(header)
            #print header
        else:
            header = headerSplit(startHeader.start_url_header, False, startHeader.login_dom) 
            wflow.append(header)   
            #print header
        for link in links:
            header =  headerSplit(link.header, link.critical_node, link.response_dom)
            wflow.append(header)
            #print header
        print wf.wflow_no
        if wf.critical == True: 
            workflows.append((wf,wflow))
        else:
            non_vworkflows.append((wf, wflow))
    #return workflows
    printWorkflows(workflows) 
    vulnerable_wflows = executeWorkflows(workflows)
    return (crawl_obj,vulnerable_wflows, non_vworkflows)
            
 
def printWorkflows(workflows):    
    for wf_obj,wflow, in workflows:
        print "workflow obj ",wf_obj.wflow_no
        for item in wflow:
            print item
            


def makePayload(data):
    dataDict = {}
    data = urllib2.unquote(data)
    #print data
    data = data.split("&")
    #print data  
    for param in data:
        value = param.split("=")
        dataDict[value[0]] = value[1]
    return dataDict


def headerSplit(header, critical, dom):
    method = ""
    url = ""
    cookie = ""
    data = ""
    header = header.strip()
    header = header.split("\n")
    method, url, http = header[0].split(" ")
    if method == "POST":
        data = makePayload(header[-1])
    for item in header:
        item = item.split(": ")
        if item[0] == "Cookie":    
            cookie = item[1]
    header = Header(method,url,cookie,data, critical,dom) 
    return header    



    
