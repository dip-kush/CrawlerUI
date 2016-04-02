# IPython log file

get_ipython().magic(u'logstart')
from crawler.models import *
id = 1
c = Crawl.objects.get(id=1)
s = StartHeader.objects.get(scan_id=c)
s
wflows = Workflow.objects.get(scan_id=c)
wflows = Workflow.objects.all(scan_id=c)
wflows = Workflow.objects.filter(scan_id=c)
wflows
wflows[1]
wflows[0]
wf = wflows[0]
wf.id
wf.wflow_no
wf.scan_id
for item in wflows:
    print item.id
    
for item in wflows:
    print item.wflow_no
    
Link.objects.get(wflow_id=wflows[1])
links = Link.objects.filter(wflow_id=wflows[1])
links
links
for item in links:
    print item.header
    
l = [3, 5, 1, 2]
get_ipython().magic(u'paste')
for wflow in wflows:
    links = Link.objects.filter(wflow_id=wflow)
    links.sort(key=lambda x:x.order_id)
    for link in links:
        header = link.split("\n")[0]
        print header
get_ipython().magic(u'paste')
for wflow in wflows:
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    for link in links:
        header = link.split("\n")[0]
        print header
get_ipython().magic(u'paste')
for wflow in wflows:
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    for link in links:
        header = link.header.split("\n")[0]
        print header
get_ipython().magic(u'paste')
for wflow in wflows:
    print wflow
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    for link in links:
        header = link.header.split("\n")[0]
        print header
s.header
get_ipython().magic(u'paste')
for wflow in wflows:
    print wflow
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    if s.login_url_header:
        print s.login_url_header.split("\n")[0]
    for link in links:
        header = link.header.split("\n")[0]
        print header
links[0]
links[0].header
h = links[0].header
get_ipython().magic(u'paste')
class Header:
    def __init__(self, method, url, cookie, data):
        self.method = method
        self.url = url
        self.cookie = cookie
        self.data = data
header = Header("POST", "http", "3435jkdfd", "param")
header.method
h.split("\n")
for item in h:
   pass

for item in h.split("\n"):
    item.split(": ")
    
for item in h.split("\n"):
    item.split(": ") print item
    
for item in h.split("\n"):
    print item.split(": ")
    
get_ipython().magic(u'paste')
def makePayload(data):
    dataDict = {}
    data = urllib2.unquote(data)
    data = data.split(&)
    for param in data:
        value = param.split("=")
        dataDict[param[0]] = param[1]
    return dataDict
def makePayload(data):
        dataDict = {}
        data = urllib2.unquote(data)
        data = data.split("&"")
        for param in data:
                value = param.split("=")
                dataDict[param[0]] = param[1]
            return dataDict
    
def makePayload(data):
        dataDict = {}
        data = urllib2.unquote(data)
        data = data.split("&")
        for param in data:
                value = param.split("=")
                dataDict[param[0]] = param[1]
            return dataDict
    
get_ipython().magic(u'paste')
def makePayload(data):
    dataDict = {}
    data = urllib2.unquote(data)
    data = data.split("&")
    for param in data:
        value = param.split("=")
        dataDict[param[0]] = param[1]
    return dataDict
get_ipython().magic(u'paste')
def headerSplit(header)
    method = ""
    url = ""
    cookie = ""
    data = ""
    header = header.strip()
    header = header.split("\n")
    method, url, http = header[0].split(" ")
    if method = "POST"
        data = makePayload(header[-1])
    for item in header:
        item = item.split(": ")
        if item=="Cookie"    
            cookie = item[1]
    header = Header(method,url,cookie,data)
    
get_ipython().magic(u'paste')
def headerSplit(header):
    method = ""
    url = ""
    cookie = ""
    data = ""
    header = header.strip()
    header = header.split("\n")
    method, url, http = header[0].split(" ")
    if method = "POST"
        data = makePayload(header[-1])
    for item in header:
        item = item.split(": ")
        if item=="Cookie"    
            cookie = item[1]
    header = Header(method,url,cookie,data)
get_ipython().magic(u'paste')
def headerSplit(header):
    method = ""
    url = ""
    cookie = ""
    data = ""
    header = header.strip()
    header = header.split("\n")
    method, url, http = header[0].split(" ")
    if method == "POST"
        data = makePayload(header[-1])
    for item in header:
        item = item.split(": ")
        if item == "Cookie"    
            cookie = item[1]
    header = Header(method,url,cookie,data)
get_ipython().magic(u'paste')
def headerSplit(header):
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
        if item == "Cookie"    
            cookie = item[1]
    header = Header(method,url,cookie,data)
get_ipython().magic(u'paste')
def headerSplit(header):
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
        if item == "Cookie":    
            cookie = item[1]
    header = Header(method,url,cookie,data)
headerSplit(h)
get_ipython().magic(u'paste')
def headerSplit(header):
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
        if item == "Cookie":    
            cookie = item[1]
    header = Header(method,url,cookie,data) 
    return header    
headerSplit(h)
final = headerSplit(h)
final
final.method
final.url
final.cookie
final.data
final.cookie
get_ipython().magic(u'paste')
def headerSplit(header):
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
    header = Header(method,url,cookie,data) 
    return header    
final = headerSplit(h)
final.cookie
final.data
final = headerSplit(s.login_url_header)
import urllib2
final = headerSplit(s.login_url_header)
final
final.method
final.url
final.data
print s.login_url_header
makePayload("e-mail=vinaysharma%40gmail&Password=vinaykool&formsubmitted=TRUE")
makePayload("e-mail=vinaysharma%40gmail&Password=vinaykool&formsubmitted=TRUE")
get_ipython().magic(u'paste')
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
makePayload("e-mail=vinaysharma%40gmail&Password=vinaykool&formsubmitted=TRUE")
final = headerSplit(s.login_url_header)
final.cookie
final.data
print s.login_url_header
get_ipython().magic(u'paste')
s.login_url_header
get_ipython().magic(u'paste')
for wflow in wflows:
    print wflow
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    if s.login_url_header:
        print headerSplit(s.login_url_header)
    else:
        print headerSplit(s.start_url_header)    
    for link in links:
        print headerSplit(link.header)
        #print header
get_ipython().magic(u'paste')
class Header:
    def __init__(self, method, url, cookie, data):
        self.method = method
        self.url = url
        self.cookie = cookie
        self.data = data

    def __str__(self):
        return self.method+" "+self.url+" "+self.data    
get_ipython().magic(u'paste')
for wflow in wflows:
    print wflow
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    if s.login_url_header:
        print headerSplit(s.login_url_header)
    else:
        print headerSplit(s.start_url_header)    
    for link in links:
        print headerSplit(link.header)
        #print header
get_ipython().magic(u'paste')
class Header:
    def __init__(self, method, url, cookie, data):
        self.method = method
        self.url = url
        self.cookie = cookie
        self.data = data

    def __str__(self):
        return self.method+" "+self.url+" "+str(self.data)    
get_ipython().magic(u'paste')
for wflow in wflows:
    print wflow
    links = Link.objects.filter(wflow_id=wflow).order_by("order_id")
    #links.sort(key=lambda x:x.order_id)
    if s.login_url_header:
        print headerSplit(s.login_url_header)
    else:
        print headerSplit(s.start_url_header)    
    for link in links:
        print headerSplit(link.header)
        #print header
exit()
