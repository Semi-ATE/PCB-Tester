# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:01:36 2020

@author: test
"""
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/scripts/', consumers.ScriptConsumer),
]
worker_channelname = consumers.RunScript