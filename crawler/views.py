from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def launch(request):
    return render(request, "index.html")


def crawlingController(request):
    if request.method == 'POST':
        print request.FILES
        login_script = request.FILES.get('login-script', None)
        login_url = request.POST.get('login-url', "")
        form_values_script = request.FILES.get('form-values-script', None)
        base_address = request.POST.get('base-address', "")
        start_url = request.POST.get('start-url', "")
        black_list_urls = request.POST.get('start-url', "")
        scope_urls = request.POST.get('scope-urls', "")
        wait_time = request.POST.get('wait_time', "")

        print login_script, login_url, form_values_script, base_address, start_url, black_list_urls, scope_urls, wait_time
        return HttpResponse("Do something")
