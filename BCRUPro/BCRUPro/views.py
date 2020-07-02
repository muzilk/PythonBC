from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from BCRUPro.models import Owner, Node


@require_GET
def index(request):
    nodes = Node.objects.all()
    context = {
        "node1": nodes[0],
        "node2": nodes[1],
        "node3": nodes[2],
        "node4": nodes[3]
    }
    return render(request, 'index.html', context=context)


@require_http_methods(['POST', 'GET'])
def create_new_node(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        # TODO: step
        owner_name = request.POST.get('owner', None)
        owner = Owner.objects.create(name=owner_name)
        device_id = request.POST.get('device_id', None)
        location = request.POST.get('location', None)
        Node.objects.create(device_id=device_id, owner=owner, location=location).save()

        return render(request, 'index.html')