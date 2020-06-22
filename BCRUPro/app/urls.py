#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from django.conf.urls import url
from django.urls import path

from app import views

urlpatterns = [
    # url(r'^$', views.hello),
    path('home/', views.home, name='home')
]
