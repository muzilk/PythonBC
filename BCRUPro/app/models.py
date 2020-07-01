from django.db import models

# Create your models here.
from django.db.models import PROTECT


class Owner(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Node(models.Model):
    device_id = models.TextField(unique=True)
    owner = models.ForeignKey(Owner, primary_key=False, blank=False, on_delete=PROTECT)
    location = models.TextField()
    today_revenue = models.BigIntegerField()
    summary_revenue = models.BigIntegerField()

    def __str__(self):
        return self.device_id


class Block(models.Model):
    block_id = models.TextField(unique=True)
    node = models.ForeignKey(Node, primary_key=False, blank=False, on_delete=PROTECT)
    revenue = models.BigIntegerField()
    create_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.block_id


