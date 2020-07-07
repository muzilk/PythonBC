from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from BCRUPro.models import Owner, Node, Block


def get_nodes_4():
    nodes = Node.objects.all()
    context = {
        "node1": nodes[0],
        "node2": nodes[1],
        "node3": nodes[2],
        "node4": nodes[3],
        "nodes": nodes
    }
    return context


def get_blocks():
    blocks = Block.objects.all()
    context = {
        "blocks": blocks
    }
    return context


def get_revenue_data():
    block_data = {}
    summary_data = {}
    for node in Node.objects.all():
        blocks = Block.objects.filter(node_id=node.id)
        revenue = []
        if blocks:
            for block in blocks:
                revenue.append(block.revenue)
            block_data.update({node.device_id: revenue})
            summary_data.update({node.device_id: sum(revenue)})
    return {"block_data": block_data, "summary_data": summary_data}


@require_GET
def index(request):
    context = get_nodes_4()
    context.update(get_revenue_data())
    return render(request, 'index.html', context=context)


@require_GET
def index2(request):
    return render(request, 'index2.html', context=get_nodes_4())


@require_GET
def index3(request):
    return render(request, 'index3.html', context=get_nodes_4())


@require_GET
def node_detail(request):
    return render(request, 'pages/examples/node-detail.html')


@require_GET
def node_edit(request):
    return render(request, 'pages/examples/node-edit.html', context=get_nodes_4())


@require_GET
def node_add(request):
    return render(request, 'pages/examples/node-add.html')


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
