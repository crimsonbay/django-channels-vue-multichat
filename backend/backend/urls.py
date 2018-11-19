"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
import chatback.views
#import debug_toolbar
from rest_framework.authtoken import views
#from django.contrib import admin

urlpatterns = [
    #path('__debug__/', include(debug_toolbar.urls)),
    # url(r'chatback/', include('chatback.urls')),
    path('api/get-chats', chatback.views.ChatListSet.as_view()),
    path('api/get-messages', chatback.views.MessageListSet.as_view()),
    path('api/add-user', chatback.views.NewUserSet.as_view()),
    path('admin/', admin.site.urls),
    path('api/leave-chat', chatback.views.LeaveChat.as_view()),
    path('api/api-token-auth/', views.obtain_auth_token),
    path('api/login', chatback.views.login),
    path('api/check-token', chatback.views.check_token),
]
