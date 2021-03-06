import Queue
import time
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from urlparse import urlparse
from GetClickables import getLinks, frameExists, getSubmitButtons,GetClickables
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from State import StateMachine, NodeData
from BeautifulSoup import BeautifulSoup
from DomComparator import getDomDiff
from logger import printRequest, clearContent
from FormExtractor import getSubmitButtonNumber, fillFormValues
from logger import LoggerHandler

logger = LoggerHandler(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#imgpath = os.path.join(BASE_DIR, 'static/screenshots')


def initState(domString, link, title, driver, globalVariables,depth,start_url,login_header):
    '''
    Initialize the State Machine adding a StateNode to fsm
    '''
    
    fsm = StateMachine()
    fsm.addHeaders(start_url, login_header, domString)
    node = NodeData()
    node.link = link
    node.domString = domString
    node.title = title
    node.visited = 0

    node.clickables = GetClickables(domString)
    for item in node.clickables:
        print item.xpath
    node.backtrackPath.append(link)
    fsm.addNode(0, node)
    imgpath = os.path.join(BASE_DIR, "static/screenshots/"+str(0)+".png")
    driver.save_screenshot(imgpath)
    if frameExists(node.domString):
        logger.info("Crawling Frames")
        crawlFrame(0, fsm, driver, globalVariables)
    else:
        Crawl(0, fsm, driver, globalVariables, depth+1)
    #clickables = graph.node[curNode]['nodedata'].clickables
    logger.info("THE END")
    drawGraph(fsm)
    return fsm



def drawGraph(fsm):
    graph = fsm.graph
    printEdges(graph)
    printNodes(graph)
    print fsm.criticalStates
    #graphJson = returnJsonGraph(graph)
    print fsm.doBacktrack
    logger.info("Number of Node Found %s" % (fsm.numberOfNodes()))
    pos = nx.spring_layout(graph)
    #labels = {k: str(k) for k in graph.nodes()}

    labels = {k: graph.node[k]['nodedata'].title for k in graph.nodes()}
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos, labels)
    #nx.draw_networkx_labels( graph ,pos, labels)
    #nx.draw(graph,node_size=3000,nodelist=graph.nodes(),node_color='b')
    #plt.show()



def backtrack(driver, fsm, node, formValues, tillEnd,path):
    logger.info("Doing backtrack")
    #driver.back()
    #if fsm.doBacktrack == False:
        #driver.back()
    #else:
    
    graph = fsm.graph
    path = graph.node[node]['nodedata'].backtrackPath
    driver.get(path[0])
    for i in range(1, len(path)-1+tillEnd):
        time.sleep(0.5)
        fillFormValues(formValues, driver)
        time.sleep(0.5)
        #action, target= path[i].split(":")
        driver.find_element_by_xpath(path[i].xpath).click()
    
    clearContent()

def AcceptAlert(driver):
    try:
        Alert(driver).accept()
    except Exception as e:
        logger.info("No Alert Box Found")


def crawlFrame(curNode, fsm, driver, globalVariables):
    menuFrame = "menu"
    bodyFrame = "body"
    graph = fsm.graph
    driver.switch_to.frame(driver.find_element_by_name(bodyFrame))
    graph.node[curNode]['nodedata'].domString = driver.page_source
    driver.switch_to.parent_frame()
    driver.switch_to.frame(driver.find_element_by_name(menuFrame))
    graph.node[curNode]['nodedata'].clickables = getLinks(driver.page_source)
    clickables = graph.node[curNode]['nodedata'].clickables
    for entity in clickables:
        tag = entity.tag
        attr = entity.attr
        attrVal = entity.attrVal
        if checkForBannedUrls(
                attrVal,
                globalVariables,
                graph.node[curNode]['nodedata'].link):
            continue

        if fsm.checkStateUrlExist(globalVariables.baseAddress+attrVal):
            continue
        logger.info("Trying to click"+attrVal)
        driver.find_element_by_xpath(
            "//"+tag+"[@"+attr+"='" + attrVal + "']").click()

        AcceptAlert(driver)
        time.sleep(2)

        driver.switch_to.parent_frame()
        driver.switch_to.frame(driver.find_element_by_name(bodyFrame))

        # code for crawling the body
        newNode = CreateNode(driver)
        # add the Node checking if the node already exists
        nodeNumber = addGraphNode(newNode,curNode,driver,fsm,entity,globalVariable.proxy_address)

        if nodeNumber != -1:
            Crawl(nodeNumber, fsm, driver, globalVariables)
        else:
            logger.info("going back frame")
            driver.back()
            #backtrack(driver,fsm,curNode,globalVariables.form      FieldValues, 1)
        driver.switch_to.parent_frame()
        #print driver.page_source
        driver.switch_to.frame(driver.find_element_by_name(menuFrame))

    #driver.back()
        #print clickableType, clickable




def Crawl(curNode, fsm, driver, globalVariables, depth):
    '''
    Crawls the Application by doing the Breadth First Search
    over the State Nodes.
    '''
    #print globalVariables.depth
    if depth > globalVariables.depth:
        logger.info("depth exceeded")
        #driver.back()
        backtrack(driver,fsm,curNode,globalVariables.formFieldValues, 0, globalVariables.proxy_address)
        return
    logger.info("crawling in normal mode")
    graph = fsm.graph
    graph.node[curNode]['nodedata'].visited = 1
    clickables = []
    clickables = graph.node[curNode]['nodedata'].clickables
    #print driver.page_source
    #print clickables
    domString = graph.node[curNode]['nodedata'].domString
    critical = checkCriticalState(domString)
    if critical:
        fsm.addCriticalState(curNode)
    logger.info("Clicking All Clickables to get a New State")
    for entity in clickables:
        #print entity.xpath
        if entity.tag == "a" and entity.attrs.has_key('href'):

            if checkForBannedUrls(
                    entity.attrs,
                    globalVariables,
                    graph.node[curNode]['nodedata'].link):
                continue

            if fsm.checkStateUrlExist(globalVariables.baseAddress+entity.attrs['href']):
                continue

        logger.info("Trying to click the element"+entity.xpath)
        time.sleep(1.5)
        fillFormValues(globalVariables.formFieldValues, driver)
        time.sleep(1.5)
        try:
            driver.find_element_by_xpath(entity.xpath).click()
        except Exception as e:
            print e

        AcceptAlert(driver)

        time.sleep(1)
        # make a new node add in the graph and the queue
        newNode = CreateNode(driver)
        # add the Node checking if the node already exists
        nodeNumber = addGraphNode(newNode,curNode,driver,fsm,entity, globalVariables.proxy_address)
        if nodeNumber != -1:
            print "crawling at depth ", str(depth+1)
            Crawl(nodeNumber, fsm, driver, globalVariables, depth+1)
        else:
            logger.info("going back click")
            backtrack(driver,fsm,curNode,globalVariables.formFieldValues, 1, globalVariables.proxy_address)
    #submitButtons = getSubmitButtons(domString)

    #submitButtonNumber = getSubmitButtonNumber(domString, driver)
    #time.sleep(2.0)
    #fillFormValues(globalVariables.formFieldValues, driver)
    #time.sleep(2.0)

    '''
    logger.info("Initiating Crawling Submit Button")
    for entity in submitButtons:
        tag = entity.tag
        attr = entity.attr
        attrVal = entity.attrVal
        tagNumber = entity.tagNumber
        logger.info("clicking %d submit button" % (tagNumber))
        print tag
        print attr
        print attrVal
        print tagNumber
        element = driver.find_element_by_xpath(
            "(//"+tag+"[@"+attr+"='"+attrVal+"'])[" + str(tagNumber+1) + "]")

        element.click()

        AcceptAlert(driver)

        time.sleep(0.5)
        newNode = CreateNode(driver)

        nodeNumber = addGraphNode(newNode,curNode,driver,fsm,entity)
        if nodeNumber != -1:
            Crawl(nodeNumber, fsm, driver, globalVariables, depth+1)
        else:
            logger.info("going back submit")
            backtrack(driver,fsm,curNode,globalVariables.formFieldValues, 1)
    WebDriverWait(driver, 2000)
    '''
    WebDriverWait(driver, 2000);
    backtrack(driver,fsm,curNode,globalVariables.formFieldValues,0, globalVariables.proxy_address)
    #print driver.page_source



def checkCriticalState(domString):
    soup = BeautifulSoup(domString)
    elements = soup.findAll('input', {'type':'password'})   
    if elements:
        return True
    return False


def checkForBannedUrls(attrs, globalVariables, currentPath):
    clickable = attrs['href']
    if clickable.find("http") != -1:
        logger.info(str(clickable) + "is a absolute link")
        path = clickable
    else:
        index = currentPath.rfind("/")
        path = currentPath[0:index] + "/" + clickable
    scopeUrls = globalVariables.scopeUrls
    baseAddress = globalVariables.baseAddress
    bannedUrls= globalVariables.bannedUrls
    flag = 0
    parsed = urlparse(clickable)
    if not parsed.hostname:
        combinedUrl = baseAddress+parsed.path
    else:
        combinedUrl = parsed.hostname+parsed.path
    print "combine url ", combinedUrl
    for item in scopeUrls:
        if item in combinedUrl:
            flag = 1
            break

    if flag == 0:
        logger.info("Exist in Banned Url " + clickable)
        return True


    if clickable in bannedUrls:
        logger.info("Exist in Banned Url " + clickable)
        return True
    else:
        for key,value in bannedUrls.iteritems():
            if attrs.has_key(key) and attrs[key]==value:
                logger.info("Exist in Banned Url " + value)
                return True
        logger.info("Path doesn't exist in Banned Url")
        return False




def printNodes(graph):
    print "----------------------Nodes---------------------"
    numberofnodes = graph.number_of_nodes()
    for i in range(numberofnodes):
        print i ,printBackTrackPath(graph.node[i]['nodedata'].backtrackPath)
    print "------------------------------------------------"

def printBackTrackPath(path):
    for entity in path:
        print entity,

'''
def printNodes(graph):
    numberofnodes = graph.number_of_nodes()
    for i in range(numberofnodes):
        print i ,graph.node[i]['nodedata'].backtrackPath
        pass
'''
def printEdges(graph):
    edges = graph.edges()
    numEdges = len(edges)
    for i in range(numEdges):
        source = edges[i][0]
        dest = edges[i][1]
        print edges[i], graph[source][dest]

def returnJsonGraph(graph):
    jsonDataFile = open("../static/jsonDataFile.txt", "w")
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

def CreateNode(driver):
    '''
    Creates a New State Node assigning the NodeData Properties
    '''
    newNode = NodeData()
    newNode.link = driver.current_url
    newNode.domString = driver.page_source
    newNode.visited = 0
    newNode.title = driver.title
    logger.info("Creating a new node with title %s" % (newNode.title))
    return newNode


def addGraphNode(newNode, curNode, driver, fsm, entity,path):
    '''
    Adding a Node to the Finite State Machine
    Checking if the Dom Tree Does Not Exist Already
    '''
    graph = fsm.graph
    curNodeUrl = graph.node[curNode]['nodedata'].link
    newNodeUrl = driver.current_url
    if curNodeUrl == newNodeUrl:
        logger.debug("found the same url %s %d" % (curNodeUrl, curNode))
        fsm.doBacktrack = True

    for item in graph.node[curNode]['nodedata'].backtrackPath:
        newNode.backtrackPath.append(item)

    newNode.backtrackPath.append(entity)

    existNodeNumber = fsm.checkNodeExists(newNode.domString)
    header = printRequest()
    if existNodeNumber == -1:
        nodeNumber = fsm.numberOfNodes()
        print "========================="
        print header
        print "========================="
        nodeNumber = fsm.numberOfNodes()
        newNode.insertedDom = getDomDiff(graph.node[curNode]['nodedata'].domString,newNode.domString)

        if curNodeUrl == newNodeUrl:
            newNode.clickables = GetClickables(newNode.insertedDom)
        else:
            newNode.clickables = GetClickables(newNode.domString)
        #print newNode.insertedDom
        #write code here
        fsm.addNode(nodeNumber, newNode)
        logger.info("Adding a New Node %d to Graph" % (nodeNumber))
        fsm.addEdges(curNode, nodeNumber, entity, header)
        logger.info(
            "Adding a Edge from Node %d and %d" %
            (curNode, nodeNumber))
        print nodeNumber, newNode.clickables
        c = newNode.clickables
        for item in c:
            print item.xpath
        time.sleep(1.5)
        imgpath = os.path.join(BASE_DIR, "static/screenshots/"+str(nodeNumber)+".png")
        driver.save_screenshot(imgpath)
        #driver.save_screenshot("../static/screenshots/" + str(nodeNumber) + ".png")
        clearContent()
        return nodeNumber
        #queue.put(nodeNumber)
    else:
        logger.info("Dom Tree Already Exist")
        #driver.save_screenshot("snaps/" + str(existNodeNumber) + ".png")
        fsm.addEdges(curNode, existNodeNumber, entity, header)
        clearContent()
        return -1
    #WebDriverWait(driver, 2000)
    #driver.back()
