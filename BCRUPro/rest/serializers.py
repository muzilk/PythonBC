from django.contrib.auth.models import User, Group
from BCRUPro.models import Order
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id', 'product', 'user_number', 'latency', 'bandwidth_down', "bandwidth_up",
                  "capacity_down", "capacity_up", "start_time", "end_time", "create_at")
