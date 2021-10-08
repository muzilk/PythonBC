from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view

from BCRUPro.models import Order
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from rest.serializers import UserSerializer, GroupSerializer
from .serializers import OrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
def orders_list(request):
    '''
    List all tasks, or create a new task.
    '''
    if request.method == 'GET':
        tasks = Order.objects.all()
        serializer = OrderSerializer(tasks, many=True)
        return Response(serializer.data)
