from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

@require_GET
def home_page(requset):
    return render(requset, '/index.html')


def home(request):
    return None