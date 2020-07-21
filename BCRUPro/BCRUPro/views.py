import random

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from BCRUPro.models import Node, Block
from login.models import User


def get_nodes(request):
    context = {}
    owner_name = request.session['user_name']
    nodes = Node.objects.filter(owner__name=owner_name)
    # nodes = Node.objects.all()
    colors = ["bg-info", "bg-success", "bg-warning", "bg-danger", "bg-orange"]
    nodesWithColors = []
    for i in range(len(nodes)):
        node = nodes[i]
        index = i % 4
        color = colors[index]
        nodesWithColors.append({'node': node, 'color': color})
    context = {
        "nodes": nodes,
        "nodesWithColors": nodesWithColors
    }
    return context


def get_blocks():
    blocks = Block.objects.all()
    context = {
        "blocks": blocks
    }
    return context


def get_revenue_data(request):
    owner_id = request.session['user_id']
    block_data = {}
    summary_data = {}

    for node in Node.objects.filter(owner_id=owner_id):
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
    context = get_nodes(request)
    context.update(get_revenue_data(request))
    context.update({"owner_name": request.session['user_name']})
    return render(request, 'index.html', context=context)


@require_GET
def index2(request):
    return render(request, 'index2.html', context=get_nodes(request))



@require_GET
def index3(request):
    return render(request, 'index3.html', context=get_nodes(request))


@require_GET
def user_manage(requset):
    users = User.objects.all()
    theader = User.get_threader()
    return render(requset, 'pages/tables/user.html', locals())


@require_GET
def block_display(requset):
    blocks = Block.objects.all()
    theader = Block.get_threader()
    return render(requset, 'pages/tables/blocks.html', locals())


@require_http_methods(['POST', 'GET'])
def create_new_node(request):
    if request.method == 'GET':
        return render(request, 'pages/examples/node-add.html')
    else:
        # TODO: step
        owner_name = request.session['user_name']
        owner = User.objects.get(name=owner_name)
        device_id = request.POST.get('device_id', None)
        location = request.POST.get('location', None)
        print("device:", device_id)
        print("location", location)
        Node.objects.create(device_id=device_id, owner=owner, location=location).save()

        return render(request, 'index.html')


@require_GET
def node_detail(request):
    return render(request, 'pages/examples/node-detail.html')


@require_GET
def node_edit(request):
    return render(request, 'pages/examples/node-edit.html', context=get_nodes(request))



