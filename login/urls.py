from django.urls import re_path as url
from login import views

app_name = 'login'

urlpatterns = [
    url(r'^login/', views.login, name="login"),
    url(r'^register/', views.register, name="register"),
    url(r'^forgot-password/', views.forgot_password, name="forgot_password"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^new-avatar/', views.new_avatar, name="new_avatar"),
]
