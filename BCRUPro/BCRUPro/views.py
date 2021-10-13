import datetime
import functools
import time
# Create your views here.
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from BCRUPro.models import *
from BCRUPro.utils import send_block
from login.models import User


def session_timeout(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        return func(request, *args, **kwargs)
    return wrapper


def get_nodes(request):
    context = {}
    try:
        owner_name = request.session['user_name']
    except KeyError:
        return render(request, 'pages/examples/login.html')
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
    owner_name = request.session['user_name']
    context.update({"owner_name": request.session['user_name']})
    owner = User.objects.get(name=owner_name)
    context.update({"owner": owner})
    return render(request, 'index.html', context=context)


@require_GET
def index2(request):
    return render(request, 'index2.html', context=get_nodes(request))


@require_GET
def index3(request):
    return render(request, 'index3.html', context=get_nodes(request))


@require_GET
def user_manage(request):
    users = User.objects.all()
    theader = User.get_threader()
    return render(request, 'pages/tables/user.html', locals())


@require_GET
def block_display(request):
    blocks = Block.objects.all()
    theader = Block.get_threader()
    owner_name = request.session['user_name']
    owner = User.objects.get(name=owner_name)
    return render(request, 'pages/tables/blocks.html', locals())


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
        Node.objects.create(device_id=device_id, owner=owner, location=location).save()

        context = get_nodes(request)
        context.update(get_revenue_data(request))
        context.update({"owner": owner})
        return render(request, 'index.html', context=context)


@require_http_methods(['POST', 'GET'])
def create_new_block(request):
    if request.method == 'GET':
        owner_name = request.session['user_name']
        owner = User.objects.get(name=owner_name)
        nodes = Node.objects.filter(owner=owner)
        return render(request, 'pages/examples/block-add.html', locals())
    else:
        node_id = request.POST.get('node_id', None)
        block_id = request.POST.get('block_id', None)
        previous_hash = request.POST.get('previous_hash', None)
        proof = request.POST.get('proof', None)
        revenue = request.POST.get('revenue', None)
        timestamp = request.POST.get('timestamp', None)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timestamp)))
        block = Block.objects.create(block_id=block_id,
                                     node=Node.objects.get(device_id=node_id),
                                     previous_hash=previous_hash,
                                     proof=proof, revenue=revenue,
                                     create_at=timestamp)
        block.save()

        blocks = Block.objects.all()
        theader = Block.get_threader()
        return render(request, 'pages/tables/blocks.html', locals())


def block_details(request):
    if request.method == 'GET':
        return render(request, 'pages/examples/block-detail.html', locals())
    else:
        block_id = request.POST.get('block_id', None)
        block = Block.objects.get(block_id=block_id)
        return render(request, 'pages/examples/block-detail.html', locals())


def block_delete(request):
    if request.method == 'POST':
        block_id = request.POST.get('block_id', None)
        block = Block.objects.get(block_id=block_id)
        block.delete()
        blocks = Block.objects.all()
        theader = Block.get_threader()
        return render(request, 'pages/tables/blocks.html', locals())


@require_GET
def node_detail(request):
    return render(request, 'pages/examples/node-detail.html')


@require_GET
def node_edit(request):
    return render(request, 'pages/examples/node-edit.html', context=get_nodes(request))


@require_GET
def invite_bids_display(request):
    try:
        owner_name = request.session['user_name']
    except KeyError:
        return render(request, 'pages/examples/login.html')
    owner = User.objects.get(name=owner_name)
    if owner.role == "customer":
        invite_bids = InviteBids.objects.filter(owner=owner)
    else:
        invite_bids = InviteBids.objects.all()
    theader = InviteBids.get_threader()
    return render(request, 'pages/examples/invite-bids-display.html', locals())


@require_http_methods(['POST', 'GET'])
def create_invite_bids(request):
    if request.method == 'GET':
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        nodes = Node.objects.filter(owner=owner)
        return render(request, 'pages/examples/invite-bids-create.html', locals())
    else:
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        invitation_id = "INBID" + now
        node_id = request.POST.get('node_id', None)
        network_type = request.POST.get('network_type', None)
        area = request.POST.get('area', None)
        i_time = request.POST.get('time', None)
        number = request.POST.get('number', None)
        data = request.POST.get('data', None)
        invite_bid = InviteBids.objects.create(invitation_id=invitation_id,
                                               owner=owner, node=Node.objects.get(device_id=node_id), 
                                               network_type=network_type, area=area, time=i_time,
                                               number=number, data=data)
        invite_bid.save()

        # send block
        feedback_message = send_block(owner_name, "csp1", invite_bid)

        if owner.role == "customer":
            invite_bids = InviteBids.objects.filter(owner=owner)
        else:
            invite_bids = InviteBids.objects.all()
        theader = InviteBids.get_threader()
        return render(request, 'pages/examples/invite-bids-display.html', locals())


@require_http_methods(['POST', 'GET'])
def offer_bids(request):
    if request.method == 'GET':
        invitation_id = request.GET.get('invitation_id', None)
        invite_bid = InviteBids.objects.get(invitation_id=invitation_id)
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        return render(request, 'pages/examples/offer-bids.html', locals())
    else:
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        
        invitation_id = request.POST.get('invitation_id', None)
        invite_bid = InviteBids.objects.get(invitation_id=invitation_id)

        price = request.POST.get('price', None)
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        bid = "BID" + now
        submit_bid = SubmitBids.objects.create(bid=bid, owner=owner, invite_bid=invite_bid, price=price)
        submit_bid.save()
        
        # send block
        feedback_message = send_block(owner_name, "csp1", invite_bid)
        
        submit_message = "sumbit success"

        return render(request, 'pages/examples/offer-bids.html', locals())


@require_http_methods(['POST', 'GET'])
def check_offers(request):
    if request.method == 'GET':
        invitation_id = request.GET.get('invitation_id', None)
        invite_bid = InviteBids.objects.get(invitation_id=invitation_id)
        submit_bids = SubmitBids.objects.filter(invite_bid=invite_bid)
        theader = SubmitBids.get_threader()

        owner_name = request.session['user_name']
        owner = User.objects.get(name=owner_name)
        return render(request, 'pages/examples/submit-bids-display.html', locals())


@require_http_methods(['POST'])
def sign_bids(request):
    bid = request.POST.get('bid', None)
    bid_obj = SubmitBids.objects.get(bid=bid)
    bid_obj.sign_status = True
    bid_obj.invite_bid.sign_status = True
    bid_obj.invite_bid.process_stat = "closed"
    bid_obj.invite_bid.winner = bid_obj.owner.name
    bid_obj.save()
    bid_obj.invite_bid.save()

    invite_bid = bid_obj.invite_bid
    submit_bids = SubmitBids.objects.filter(invite_bid=invite_bid)
    theader = SubmitBids.get_threader()
    owner_name = request.session['user_name']
    owner = User.objects.get(name=owner_name)
    # send block
    feedback_message = send_block(owner_name, "csp1", bid_obj.invite_bid)
    
    return render(request, 'pages/examples/submit-bids-display.html', locals())


@require_http_methods(['POST', 'GET'])
def deploy_bids(request):
    if request.method == 'GET':
        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        invitation_id = request.POST.get('invitation_id', None)
        invite_bid = InviteBids.objects.get(invitation_id=invitation_id)
        invite_bid.deploy_status = True
        invite_bid.save()
        owner_name = request.session['user_name']
        owner = User.objects.get(name=owner_name)
        return render(request, 'pages/examples/invite-bids-deploy.html', locals())
    

@require_http_methods(['GET', "POST"])
def mall(request):
    if request.method == 'GET':
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        product1 = Product.objects.all()[0:3]
        product2 = Product.objects.all()[3:]
        owner_name = request.session['user_name']
        owner = User.objects.get(name=owner_name)
        return render(request, 'pages/examples/mall.html', locals())


@require_http_methods(['GET'])
def vendor_display(request):
    if request.method == 'GET':
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        product_name = request.GET.get('product_name', None)
        product = Product.objects.get(name=product_name)
        vendors = Vendor.objects.filter(category__name=product_name)
        theader = Vendor.get_threader()
        return render(request, 'pages/examples/vendor_display.html', locals())


@require_http_methods(['POST'])
def sign_order(request):
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name', None)
        vendor = Vendor.objects.get(name=vendor_name)
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        return render(request, 'sign_order.html', locals())


@require_http_methods(['POST'])
def buy(request):
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name', None)
        user_number = int(request.POST.get('user_number', 0))
        latency = int(request.POST.get('latency', 0))
        bandwidth_down = int(request.POST.get('bandwidth_down', 0))
        bandwidth_up = int(request.POST.get('bandwidth_up', 0))
        capacity_down = int(request.POST.get('capacity_down', 0))
        capacity_up = int(request.POST.get('capacity_up', 0))
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M")

        order_id = "ORD%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        order = Order.objects.create(order_id=order_id, vendor=Vendor.objects.get(name=vendor_name),
                                     user_number=user_number, latency=latency, bandwidth_down=bandwidth_down,
                                     bandwidth_up=bandwidth_up, capacity_down=capacity_down, capacity_up=capacity_up,
                                     start_time=start_time, end_time=end_time)
        order.save()

        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        orders = Order.objects.all()
        theader = Order.get_threader()
        return render(request, 'order_display.html', locals())


@require_GET
def order_display(request):
    orders = Order.objects.all()
    theader = Order.get_threader()
    try:
        owner_name = request.session['user_name']
    except KeyError:
        return render(request, 'pages/examples/login.html')
    owner = User.objects.get(name=owner_name)
    return render(request, 'order_display.html', locals())


@require_POST
def order_detail(request):
    order_id = request.POST.get('order_id', None)
    order = Order.objects.get(order_id=order_id)

    delta = order.end_time-order.start_time
    hours = delta.days * 24 + delta.seconds / 3600

    vswirch_count = 1
    vswirch_vcpu = 11 - int(order.latency / 10)
    vswirch_ram = int(order.bandwidth_up / 10)

    rounting_agent_count = 1
    rounting_agent_vcpu = int(vswirch_vcpu / 10) + 1
    rounting_agent_ram = 8

    data_plane_link_count = order.user_number
    data_plane_link_vcpu = 1
    data_plane_link_ram = int(order.capacity_up / 20) + 1

    key_value_database_rount = 1
    key_value_database_vcpu = 1
    key_value_database_ram = order.user_number

    common_service_adp_count = 1
    common_service_adp_vcpu = 1
    common_service_adp_ram = 3

    vcpu_per_network = \
        rounting_agent_count * rounting_agent_vcpu + \
        data_plane_link_count * data_plane_link_vcpu + \
        vswirch_count * vswirch_vcpu + \
        key_value_database_rount * key_value_database_vcpu + \
        common_service_adp_count * common_service_adp_vcpu

    ram_per_network = \
        rounting_agent_count * rounting_agent_ram + \
        data_plane_link_count * data_plane_link_ram + \
        vswirch_count * vswirch_ram + \
        key_value_database_rount * key_value_database_ram + \
        common_service_adp_count * common_service_adp_ram

    price_per_hour = vcpu_per_network*0.05 + ram_per_network*0.015
    price = price_per_hour*hours

    price_per_hour = "%.3f" % price_per_hour
    price = "%.3f" % price

    try:
        owner_name = request.session['user_name']
    except KeyError:
        return render(request, 'pages/examples/login.html')
    owner = User.objects.get(name=owner_name)
    return render(request, 'order_details.html', locals())


@require_POST
def order_delete(request):
    order_id = request.POST.get('order_id', None)
    order = Order.objects.get(order_id=order_id)
    order.delete()
    orders = Order.objects.all()
    theader = Order.get_threader()
    try:
        owner_name = request.session['user_name']
    except KeyError:
        return render(request, 'pages/examples/login.html')
    owner = User.objects.get(name=owner_name)
    return render(request, 'order_display.html', locals())


@require_http_methods(['GET'])
def agriculture(request):
    if request.method == 'GET':
        try:
            owner_name = request.session['user_name']
        except KeyError:
            return render(request, 'pages/examples/login.html')
        owner = User.objects.get(name=owner_name)
        owner_name = request.session['user_name']
        owner = User.objects.get(name=owner_name)
        crops = Crops.objects.all()
        return render(request, 'pages/examples/agriculture.html', locals())


@require_http_methods(['GET'])
def product_detail(request):
    if request.method == 'GET':
        product_name = request.GET.get("product_name", None)
        crop = Crops.objects.get(name=product_name)
        return render(request, 'pages/examples/product-detail.html', locals())
