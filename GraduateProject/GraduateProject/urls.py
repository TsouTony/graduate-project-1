"""GraduateProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from main.views import main, login, logout, blog, imgDetail, addComment
from django.contrib.auth import views


urlpatterns = [
    # 後台控制界面
    path('admin/', admin.site.urls),
    path('main/', main, name = 'main'),
    # blog url
    path('blog/<str:user>', blog, name = 'blog'),
    # imgDetail url
    path('blog/<str:user>/<str:imgID>', imgDetail, name = 'imgDetail'),
    # 新增commend url
    path('blog/addComment', addComment, name = 'addComment'),
    # 登入url
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    # 登出url
	path('accounts/logout/', logout, name = 'logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
