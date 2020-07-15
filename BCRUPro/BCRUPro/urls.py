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

import datetime
from django.contrib import admin
from django.urls import path, re_path, include
from BCRUPro.views import *

app_name = 'BCRUPro'


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', index, name='index'),
    re_path(r'^index2', index2, name='index2'),
    re_path(r'^index3', index3, name='index3'),
    re_path(r'^nodeDetail', node_detail, name='node_detail'),
    re_path(r'^nodeAdd', node_add, name='node_add'),
    re_path(r'^nodeEdit', node_edit, name='node_edit'),
    re_path(r'^login', login, name='login'),
    re_path(r'^register', register, name='register'),
    re_path(r'^forgot_password', forgot_password, name='forgot_password'),
    re_path(r'^user_manage', user_manage, name='user_manage'),
    re_path(r'^user_blocks', user_blocks, name='user_blocks')
]
