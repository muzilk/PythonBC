import hashlib

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods, require_GET

from BCRUPro.views import get_nodes, get_revenue_data
from login.models import User


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


@require_http_methods(['POST', 'GET'])
def login(request):
    # if request.session.get('is_login', None):
    #     context = get_nodes(request)
    #     context.update(get_revenue_data(request))
    #     return render(request, 'index.html', context=context)

    if request.method == 'GET':
        return render(request, 'pages/examples/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            print(e)
            user = None
        if user is not None:
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                context = get_nodes(request)
                context.update(get_revenue_data(request))
                owner = User.objects.get(name=user.name)
                context.update({"owner": owner})
                return render(request, 'index.html', context=context)
            else:
                return render(request, 'pages/examples/login.html', {"message": "Password is error"})
        else:
            return render(request, 'pages/examples/login.html', {"message": "Account is not exist"})


@require_http_methods(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return render(request, 'pages/examples/register.html')
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'pages/examples/register.html', {"message": "The two passwords do not match"})
        else:
            same_name_user = User.objects.filter(name=name)
            if same_name_user:
                return render(request, 'pages/examples/register.html', {"message": "The user name is exist"})
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                return render(request, 'pages/examples/register.html', {"message": "The email is registered"})

            new_user = User.objects.create()
            new_user.name = name
            new_user.email = email
            new_user.password = hash_code(password)
            new_user.role = role
            new_user.save()
            return render(request, 'pages/examples/login.html')


@require_GET
def forgot_password(request):
    return render(request, 'pages/examples/forgot-password.html')


@require_GET
def logout(request):
    request.session.flush()
    return render(request, 'pages/examples/login.html')
