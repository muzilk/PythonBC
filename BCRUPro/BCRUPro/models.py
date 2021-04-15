from django.db import models

# Create your models here.
from django.db.models import PROTECT

from login.models import User


class Node(models.Model):
    device_id = models.TextField(unique=True)
    owner = models.ForeignKey(User, primary_key=False, blank=False, on_delete=PROTECT)
    location = models.TextField()
    today_revenue = models.BigIntegerField(default=0)
    summary_revenue = models.BigIntegerField(default=0)

    @staticmethod
    def get_threader():
        return ["Device ID", "Owner", "Location", "Today Revenue", "Summary Revenue"]

    def __str__(self):
        return self.device_id


class Block(models.Model):
    block_id = models.TextField(unique=True)
    node = models.ForeignKey(Node, primary_key=False, blank=False, on_delete=PROTECT)
    previous_hash = models.TextField(default="1")
    proof = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_created=True)

    @staticmethod
    def get_threader():
        return ["ID", "Node", "Revenue", "Create Time"]

    def __str__(self):
        return self.block_id


class InviteBids(models.Model):
    process_stat = (
        ('opening', 'opening'),
        ('closed', 'closed'),
    )
    invitation_id = models.TextField(unique=True)
    owner = models.ForeignKey(User, primary_key=False, blank=False, on_delete=PROTECT)
    node = models.ForeignKey(Node, primary_key=False, blank=False, on_delete=PROTECT)
    network_type = models.TextField()
    area = models.TextField()
    time = models.TextField()
    number = models.TextField()
    data = models.TextField()
    sign_status = models.BooleanField(default=False)
    deploy_status = models.BooleanField(default=False)
    verify_status = models.BooleanField(default=False)
    winner = models.TextField()
    process_status = models.CharField(max_length=32, choices=process_stat, default='opening')
    create_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_threader():
        return ["ID", "Node", "Network Type", "Area", "Time", "Number", "Data", "Create Time", "Winner"]

    def __str__(self):
        return self.invitation_id


class SubmitBids(models.Model):
    bid = models.TextField(unique=True)
    owner = models.ForeignKey(User, primary_key=False, blank=False, on_delete=PROTECT)
    invite_bid = models.ForeignKey(InviteBids, primary_key=False, blank=False, on_delete=PROTECT)
    price = models.IntegerField()
    sign_status = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_threader():
        return ["BID", "Price", "Create Time", "Status"]

    def __str__(self):
        return self.bid


class Product(models.Model):
    name = models.TextField(unique=True)
    image_name = models.TextField(unique=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_static_image(self):
        return "adminlte/dist/img/"+self.image_name

    @staticmethod
    def get_image_basename(name):
        return name.split("/")[-1]


class Order(models.Model):
    order_id = models.TextField(unique=True)
    product = models.ForeignKey(Product, primary_key=False, blank=False, on_delete=PROTECT)
    user_number = models.IntegerField(default=0)
    latency = models.IntegerField(default=0)
    bandwidth_down = models.IntegerField(default=0)
    bandwidth_up = models.IntegerField(default=0)
    capacity_down = models.IntegerField(default=0)
    capacity_up = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    @staticmethod
    def get_threader():
        return ["Order", "Product", "Users Number", "Latency", "Bandwidth Down", 
                "Bandwidth Up", "Capacity Down", "Capacity Up", "Create Time"]

