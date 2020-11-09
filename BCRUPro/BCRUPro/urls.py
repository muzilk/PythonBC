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

from login.views import login
from BCRUPro.views import *

app_name = 'BCRUPro'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    path('login/', include('login.urls', namespace="login")),


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
]
