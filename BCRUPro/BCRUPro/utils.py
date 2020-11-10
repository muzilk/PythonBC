#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests


def send_block(sender, recipient, hash, timestart="20201108", timeend="20201111", ):
    url = "http://52.81.51.103:5000/transaction/new"
    headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/json',
    }
    data = '{"sender": "{}", "recipient": "{}", "timestart": "{}", "timeend": "{}", "data": "{}"}'.format(sender, recipient, timestart, timeend, hash)
    requests.post(url=url, headers=headers, data=data)
