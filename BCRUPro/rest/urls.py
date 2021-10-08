from django.urls import include, path
from django.conf.urls import url
from . import views
app_name = 'rest'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^orders/$', views.orders_list, name='order_list'),
]