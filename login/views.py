import hashlib
import os

from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from CatOnClouds.settings import USER_ROOT
from login.models import User


# Create your views here.

def hash_code(s, salt='catonclouds'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


@require_http_methods(['POST', 'GET'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
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
                request.session['email'] = user.email
                request.session['name'] = user.name
                return render(request, "home-page.html", locals())
            else:
                return render(request, 'login/login.html', {"message": "Password is error"})
        else:
            return render(request, 'login/login.html', {"message": "Account is not exist"})


@require_http_methods(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    else:
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'login/register.html', {"message": "The two passwords do not match"})
        else:
            same_name_user = User.objects.filter(email=email)
            if same_name_user:
                return render(request, 'login/register.html', {"message": "The user name is exist"})
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                return render(request, 'login/register.html', {"message": "The email is registered"})

            new_user = User.objects.create()
            new_user.email = email
            new_user.name = name
            new_user.password = hash_code(password)
            new_user.save()
            avatar_path = os.path.join(USER_ROOT, str(new_user.id))
            if not os.path.exists(avatar_path):
                os.mkdir(avatar_path)

            return render(request, 'login/login.html')


@require_http_methods(['POST', 'GET'])
def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'login/forgot-password.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'login/forgot-password.html', {"warning": "The two passwords do not match"})
        else:
            user = User.objects.get(email=email)
            user.password = hash_code(password)
            user.save()
            return render(request, 'login/forgot-password.html', {"info": "The password is reset"})


@require_GET
def logout(request):
    request.session.flush()
    return render(request, 'login/login.html')


@require_http_methods(['POST', 'GET'])
def profile(request):
    if request.method == 'GET':
        user = User.objects.get(email=request.session['email'])
        return render(request, 'login/profile.html', locals())
    else:
        email = request.POST.get('email', None)
        name = request.POST.get('name', None)
        user = User.objects.get(email=request.session['email'])
        if email:
            user.email = email
        if name:
            user.name = name
        user.save()
        return render(request, 'login/profile.html', locals())


@require_POST
def new_avatar(request):
    user = User.objects.get(email=request.session['email'])
    new_avatar = request.FILES.get("new_avatar", None)
    filename = "avatar.png"
    save_path = os.path.join(USER_ROOT, str(user.id))
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(os.path.join(save_path, filename), "wb") as fw:
        for c in new_avatar.chunks():
            fw.write(c)
    return render(request, 'login/profile.html', locals())
