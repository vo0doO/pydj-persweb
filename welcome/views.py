import os

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from welcome.models import PageView, WelcomePage, WelcomePageBlock

from . import database


# Create your views here.
def readme(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/include/html/organism/readme.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    request_time = timezone.now()
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[-1]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    ip = get_client_ip(request)
    PageView.objects.create(hostname=hostname, ip=ip)
    sections = get_list_or_404(WelcomePageBlock)
    
    return render(request, 'welcome/include/html/molecule/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count(),
        'sections': sections,
    })

def health(request):
    return HttpResponse(PageView.objects.count())
