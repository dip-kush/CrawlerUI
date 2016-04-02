from django.db import models

# Create your models here.

class Crawl(models.Model):
    login_script = models.FileField(upload_to='uploads')
    form_values_script = models.FileField(upload_to = 'uploads')
    login_url = models.CharField(max_length=100,default=None)
    base_address = models.CharField(max_length=100,default=None)
    start_url = models.CharField(max_length=100,default=None)
    black_list_urls = models.CharField(max_length=100,default=None)
    scope_urls = models.CharField(max_length=100,default=None)
    wait_time = models.CharField(max_length=100,default=None)
    depth = models.CharField(max_length=5, default="100")
    def __str__(self):
        return str(self.id)


class Workflow(models.Model):
    scan_id = models.ForeignKey(Crawl)
    wflow_no = models.IntegerField()
    def __str__(self):
        return str(self.wflow_no)
   

class StartHeader(models.Model):
    scan_id = models.ForeignKey(Crawl)
    start_url_header = models.CharField(max_length=1000, default="")
    #start_method = models.CharField(max_length="5",default="")
    #start_url = models.CharField(max_length="200",default="")
    #start_data = models.CharField(max_length="200",default="")
    #start_cookie = models.TextField()
    #start_dom = models.TextField()
    login_url_header = models.CharField(max_length=1000, default="") 
    #login_method = models.CharField(max_length="200",default="")
    #login_url = models.CharField(max_length="200",default="")
    #login_data = models.CharField(max_length="200", default="")
    #login_cookie = models.TextField()
    login_dom = models.TextField()
    def __str__(self):
        return str(self.id)

class Link(models.Model):	
    wflow_id = models.ForeignKey(Workflow)
    link = models.CharField(max_length=200, default="")
    order_id = models.IntegerField()
    header = models.CharField(max_length=500, default="")
    #method = models.CharField(max_length="200",default="")
    #url = models.CharField(max_length="200",default="")
    #data = models.CharField(max_length="200", default="")
    #cookie = models.TextField()
    response_dom = models.TextField()
    def __str__(self):    
        return str(self.link)
    

'''

    request_header = models.CharField(max_length=200, default="")
    cookie = models.CharField(max_length=200, default="")
    query_param = models.CharField(max_length=200, default="")


'''	
