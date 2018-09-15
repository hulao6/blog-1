"""
blog URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from django.views.generic.base import RedirectView
from blog.settings import MEDIA_ROOT
from django.conf import settings
from article.views import upload_image


######################################
# 入口 URL
######################################
urlpatterns = [
    path('admin4blog/', admin.site.urls),

    # favicon.ico
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),

    # 静态文件
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),

    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # article
    path('', include('article.urls')),

    # CKeditor上传图片
    path('uploadimg/', upload_image),
]
