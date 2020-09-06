"""BlogYee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
import post.views as views_post
import paint.views as views_paint
import post.views_github as views_github

urlpatterns = [
    path(r'git_update/',views_github.github_hello),
    path(r'', views_post.displayHome),
    path(r'category/',views_post.categoryView),
    path(r'documents/<path:article_dir>/',views_post.postView),
    path(r'3dview/',views_post.display3d),
    path(r'admin/', admin.site.urls),
    path(r'paint/',views_paint.displayAllPaint),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
