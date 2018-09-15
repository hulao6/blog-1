"""
article admin
"""
from django.contrib import admin
from .models import *


######################################
# 后台注册
######################################
admin.site.register(Banner)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Subject)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentReplay)
admin.site.register(FriendLink)
admin.site.register(Partner)
