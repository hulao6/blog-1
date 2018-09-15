"""
article forms
"""
from django import forms
from .models import *


######################################
# 添加文章表单
######################################
class AddArticleForm(forms.Form):
    title = forms.CharField(min_length=4, max_length=100, required=True)


######################################
# 添加文章评论
######################################
class AddArticleCommentForm(forms.Form):
    comment = forms.CharField(min_length=4, max_length=200, required=True)
    email = forms.EmailField(required=True)
