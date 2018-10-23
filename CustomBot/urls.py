"""CustomBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from admin_panel import views

urlpatterns = [
    #url(r'/', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'index/', views.index, name='index'),
    url(r'filters/', views.filters, name='filters'),
    url(r'create_filter/', views.create_filter, name='create_filter'),
    url(r'add_channel/', views.add_channel, name='add_channel'),
    url(r'channels_list/', views.channels_list, name='channel_list'),
    url(r'login/', views.login, name="login"),
    url('logout/', views.logout, name='logout'),
    url(r'user_settings/', views.user_settings, name='user_settings'),
    path(r'channel_details/<int:id>/', views.channel_details, name='channel_details'),
    path(r'edit_channel/<int:id>', views.edit_channel, name='edit_channel')
]
