import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Crawler import initState
from FormExtractor import getFormFieldValue
from BeautifulSoup import BeautifulSoup
from logger import LoggerHandler
from selenium.webdriver.common.proxy import *
from logger import printRequest, clearContent
import time
import HTMLParser



h = HTMLParser.HTMLParser()
logger = LoggerHandler(__name__)


class Globals:
    '''
    Contains initialization of all the global variables
    '''

    def __init__(self):
        self.formFieldValues = {'id': {} , 'xpath': {}, 'name': {}}
        self.bannedUrls = {}
        self.scopeUrls = []
        self.waitTime= 0
        self.baseAddress = ""
        self.depth = 100 #infinite depth
        self.proxy_address = ""

    def getFormValues(self, filePath=None, fileHandler=None):
        self.formFieldValues = getFormFieldValue(filePath,fileHandler)

    def addBlackList(self, urls):
        urls = urls.split(',')
        for url in urls:
            print url
            key, value = url.split(":")
            self.bannedUrls[key] = value

    def setGlobalWait(self, time):
        self.waitTime = time

    def setDepth(self, depth):
        self.depth = depth

    def addScopeUrl(self, urls):
        self.scopeUrls = urls.split(",")

    def addBaseAddress(self, baseAddress):
        self.baseAddress = baseAddress
    
    def setProxy(self, address):
        self.proxy_address = address


   
def doLogin(login_url, driver, path, scriptFilePath=None, scriptFileHandler=None):
    print "doing login"
    print login_url
    driver.get(login_url)
    start_header = printRequest()
    print "========================="
    print start_header
    print "========================="
    time.sleep(2)
    clearContent()

    if scriptFilePath:
        f = open(scriptFilePath)
    else:
        f = scriptFileHandler
    bs = BeautifulSoup(f)
    #print bs
    l = bs.findAll("tr")
    print len(l)
    for i in range(1, len(l)):
        type = l[i].findAll("td")[0].text
        target = l[i].findAll("td")[1].text
        value = l[i].findAll("td")[2].text
        #print type, target, value
        if value == "" and type == "clickAndWait":
            findSelector(driver,type,target,value)
            #element = driver.find_element_by_xpath(
            #"(//input[@type='submit'])")
            #element.click()
        elif value != "":
            #print value
            target = str(target)
            index = str(target).find('=')
            type = target[0:index]
            fieldVal = target[index + 1:]
            if type == "id":
                element = driver.find_element_by_id(fieldVal)
                element.send_keys(value)
            elif type == "name":
                driver.find_element_by_name(fieldVal).send_keys(value)
            else:
                driver.find_element_by_xpath(fieldVal).send_keys(value)
    time.sleep(2)
    login_header = printRequest()
    print "========================="
    print login_header
    print "========================="
    clearContent()
    return (start_header, login_header)
        
''' 
def printRequest(path):
    #path = "/home/deepak/programs/proxy/requests.txt"
    data = ""
    try:
        f = open(path, "r")
        data = f.readlines()
        data = ''.join(data)
    except Exception as e:
        print e
    if data.find("HEADEREND")!=-1:
        data = data.strip("HEADEREND")
        headers = data.split("HEADEREND")
        header = headers[0].strip()
        header = header.replace("\r", "")
        header = header.replace("\n\n", "\n")
        return header
    else:
        headers = data.split("RESPONSEHEADERS")
        header = headers[0].strip()
        header = header.replace("\r", "")
        header = header.replace("\n\n", "\n")
        return header


def clearContent(path):
    try:
        #path = "/home/deepak/programs/proxy/requests.txt"
        f = open(path, "w")
    except Exception as e:
        print e
 
''' 

def findSelector(driver, type,target,value):
    target = str(target)
    index = str(target).find('=')
    type = target[0:index]
    fieldVal = target[index + 1:]
    fieldVal = h.unescape(fieldVal)
    print fieldVal
    if type == "id":
        driver.find_element_by_id(fieldVal).click()
    elif type == "name":
        driver.find_element_by_name(fieldVal).click()
    elif type == "css":
        driver.find_element_by_css_selector(fieldVal).click()
    else:
        driver.find_element_by_xpath(fieldVal).click()



def initializeParams(crawling_spec):
    login_url = None
    start_header = ""
    login_header = ""
    globalVariables = Globals()

    # globalVariables.bannedUrls.append("http://127.0.0.1:81/login/profile.html")

    #driver = webdriver.PhantomJS()
    myProxy = "localhost:8081"

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': '' # set this value as desired
    })

    driver = webdriver.Firefox(proxy = proxy)
    #driver = webdriver.Chrome()
    logger.info("Browser is Launched")
    #driver.get("http://127.0.0.1:81/login/login.php")

    '''
    if crawling_spec["proxy_address"]:
        globalVariables.setProxy(crawling_spec["proxy_address"])
    '''


    if crawling_spec["login_url"]:
        login_url = crawling_spec["login_url"]

    if crawling_spec["login_script"]:
        #print crawling_spec["login_script"].readlines()
        logger.info("Logging in Application")
        if not login_url:
            logger.error("No Login URL provided")
        else:
            print "performing login"
            start_header, login_header = doLogin(login_url, driver, globalVariables.proxy_address,scriptFileHandler = crawling_spec["login_script"] )

    if crawling_spec["form_values_script"]:
        globalVariables.getFormValues(fileHandler = crawling_spec["form_values_script"])

    if crawling_spec["base_address"]:
        globalVariables.addBaseAddress(crawling_spec["base_address"])


    if crawling_spec["start_url"]:
        driver.get(crawling_spec["start_url"])

    if crawling_spec["scope_urls"]:
        globalVariables.addScopeUrl(crawling_spec["scope_urls"])

    if crawling_spec["black_list_urls"]:
        globalVariables.addBlackList(crawling_spec["black_list_urls"])

    if crawling_spec["depth"]:
        globalVariables.setDepth(int(crawling_spec["depth"]))

    if not crawling_spec["start_url"] and not crawling_spec["login_url"]:
        logger.error("No Start Url Provided not Login Url Provided")
        return

    if crawling_spec["wait_time"]:
        globalVariables.setGlobalWait(crawling_spec["wait_time"])


   
    # time.sleep(5)
    # move the controller to Initiate Crawler Activity
    logger.info("Initiating the Crawler")
    fsm = initState(
        driver.page_source,
        driver.current_url,
        driver.title,
        driver,
        globalVariables,0, start_header, login_header)

    #assert "Welcome, " in driver.page_source
    driver.close()

    print "graph obj",fsm.graph.nodes()
    return fsm


def somefunc():
    pass

def main():
    '''
    crawls the demo website http://127.0.0.1:81/login/login.php
    with login credentials
    email = vinaysharma@gmail
    password = vinaykool
    '''
    login_url = None
    start_header = ""
    login_header = ""
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--login-script", action="store", dest="login_script", help="Path to python login script")
    parser.add_argument("-u", "--login-url", action="store", dest="login_url", help="Login Page Url")
    parser.add_argument("-f", "--form-script", action="store", dest="form_values_script", help="Path to Form Values Script")
    parser.add_argument("-b", "--base-address", action="store", dest="base_address", help="Base address")
    parser.add_argument("-s", "--start-url", action="store", dest="start_url", help="Starting Page Url")
    parser.add_argument("-bl", "--black-list", action="store", dest="black_list_urls", help="Black List Urls")
    parser.add_argument("-sc", "--scope", action="store", dest="scope_url", help="scope of the crawler")
    parser.add_argument("-d", "--depth", action="store", dest="depth",help="depth of crawl", type=int)
    parser.add_argument("-p", "--proxy", action="store", dest="proxy_address",help="proxy address")
    parser.add_argument('-t', action="store", dest="time", type=int)

    args = parser.parse_args()

    globalVariables = Globals()

    proxy_address = ""
    # globalVariables.bannedUrls.append("http://127.0.0.1:81/login/profile.html")

    #driver = webdriver.PhantomJS()
    myProxy = "localhost:8081"

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': '' # set this value as desired
    })

    driver = webdriver.Firefox(proxy = proxy)
    #driver = webdriver.Chrome()
    logger.info("Browser is Launched")
    #driver.get("http://127.0.0.1:81/login/login.php")
    
    if args.proxy_address:
        proxy_address = args.proxy_address

    if args.login_url:
        login_url = args.login_url

    if args.login_script:
        logger.info("Logging in Application")
        if not login_url:
            logger.error("No Login URL provided")
        else:
            start_header, login_header = doLogin(login_url, driver,proxy_address, scriptFilePath = args.login_script)

    if args.form_values_script:
        globalVariables.getFormValues(args.form_values_script)

    if args.base_address:
        globalVariables.addBaseAddress(args.base_address)

    if args.depth:
        globalVariables.setDepth(args.depth)

    if args.start_url:
        driver.get(args.start_url)

    if args.scope_url:
        globalVariables.addScopeUrl(args.scope_url)

    if args.black_list_urls:
        globalVariables.addBlackList(args.black_list_urls)

    if not args.start_url and not args.login_url:
        logger.error("No Start Url Provided not Login Url Provided")
        return

    if args.time:
        globalVariables.setGlobalWait(args.time)

    # time.sleep(5)
    # move the controller to Initiate Crawler Activity
    logger.info("Initiating the Crawler")
    initState(
        driver.page_source,
        driver.current_url,
        driver.title,
        driver,
        globalVariables,0, start_header, login_header)

    #assert "Welcome, " in driver.page_source
    driver.close()


if __name__ == '__main__':
    main()
