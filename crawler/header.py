class Header:
    def __init__(self, method, url, cookie, data, critical, dom):
        self.method = method
        self.url = url
        self.cookie = cookie
        self.data = data
        self.critical = critical
        self.dom = dom        

    def __str__(self):
        return self.method+" "+self.url+" "+str(self.data)+" "+str(self.critical)    
