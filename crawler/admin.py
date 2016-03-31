from django.contrib import admin
from models import Crawl, Workflow, Link,StartHeader
# Register your models here.

admin.site.register(Crawl)
admin.site.register(Workflow)
admin.site.register(Link)
admin.site.register(StartHeader)

