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
