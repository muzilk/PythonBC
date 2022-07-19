"""BCRUPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from BCRUPro.views import *
from rest_framework import routers
from login.views import login
from rest.views import *

app_name = 'BCRUPro'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    path('login/', include('login.urls', namespace="login")),
    path('', include(router.urls)),
    path('api/', include('rest.urls', namespace="rest")),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^index', index, name='index'),
    re_path(r'^index2', index2, name='index2'),
    re_path(r'^index3', index3, name='index3'),
    re_path(r'^nodeDetail', node_detail, name='node_detail'),
    re_path(r'^create_new_node', create_new_node, name='create_new_node'),
    re_path(r'^nodeEdit', node_edit, name='node_edit'),

    re_path(r'^user_manage', user_manage, name='user_manage'),
    re_path(r'^block_display', block_display, name='block_display'),
    re_path(r'^block_details', block_details, name='block_details'),
    re_path(r'^block_delete', block_delete, name='block_delete'),
    re_path(r'^create_new_block', create_new_block, name='create_new_block'),

    re_path(r'^invite_bids_display', invite_bids_display, name='invite_bids_display'),
    re_path(r'^create_invite_bids', create_invite_bids, name='create_invite_bids'),
    re_path(r'^offer_bids', offer_bids, name='offer_bids'),
    re_path(r'^check_offers', check_offers, name='check_offers'),
    re_path(r'^sign_bids', sign_bids, name='sign_bids'),
    re_path(r'^deploy_bids', deploy_bids, name='deploy_bids'),

    re_path(r'^mall', mall, name='mall'),
    re_path(r'^sign_order', sign_order, name='sign_order'),
    re_path(r'^vendor_display', vendor_display, name='vendor_display'),
    re_path(r'^order_delete', order_delete, name='order_delete'),
    re_path(r'^buy', buy, name='buy'),
    re_path(r'^order_display', order_display, name='order_display'),
    re_path(r'^order_detail', order_detail, name='order_detail'),

    re_path(r'^agriculture', agriculture, name='agriculture'),
    re_path(r'^product_detail', product_detail, name='product_detail'),

    re_path(r'^get_crops_data', get_crops_data, name='get_crops_data'),
    re_path(r'^update_crops_data', update_crops_data, name='get_crops_data'),
    re_path(r'^crops_deploy', crops_deploy, name='crops_deploy'),
    re_path(r'^get_deploy_status', get_deploy_status, name='get_deploy_status'),
    re_path(r'^search_deploy_crop', search_deploy_crop, name='search_deploy_crop'),
    re_path(r'^update_deploy_status', update_deploy_status, name='update_deploy_status'),
]
