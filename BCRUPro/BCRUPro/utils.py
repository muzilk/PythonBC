#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import hashlib
import json

import requests


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def send_block(sender, recipient, invite_bid):
    url = "http://52.81.51.103:5000/transaction/new"
    headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/json',
    }
    bid_context = "{}:{}:{}:{}:{}:{}:{}:{}".format(invite_bid.invitation_id, invite_bid.owner, invite_bid.node_id,
                                                   invite_bid.network_type, invite_bid.area, invite_bid.time,
                                                   invite_bid.number, invite_bid.data)

    now = datetime.datetime.now()
    offset = datetime.timedelta(hours=+1)
    timestart = now.strftime('%Y-%m-%d %H:%M:%S')
    timeend = (now + offset).strftime('%Y-%m-%d %H:%M:%S')

    hash_str = hash_code(bid_context)
    
    data = {"sender": sender, "recipient": recipient, "timestart": timestart, "timeend": timeend, "data": hash_str}
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        return response.text
    except Exception as e:
        print(e)
        return e
