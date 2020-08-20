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


