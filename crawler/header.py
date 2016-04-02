class Header:
    def __init__(self, method, url, cookie, data):
        self.method = method
        self.url = url
        self.cookie = cookie
        self.data = data

    def __str__(self):
        return self.method+" "+self.url+" "+str(self.data)    
