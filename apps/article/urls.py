"""
article URL Configuration
"""
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from .views import *


app_name = 'article'

######################################
# article URL
######################################
urlpatterns = [
    # 首页
    path('', IndexView.as_view(), name='index'),

    # 写文章
    path('article/write.html', WriteArticleView.as_view(), name='article_write'),

    # 文章详情
    path('detail/<int:art_id>.html', DetailView.as_view(), name='article_detail'),

    # 文章点赞
    path('detail/like.html', ArticleLikeView.as_view(), name='article_like'),

    # 评论文章
    path('article/comment.html', ArticleCommentView.as_view(), name='article_comment'),

    # 文章列表
    path('article/list/<str:list_name>.html', ArticleListView.as_view(), name='article_list'),

    # 专题首页
    path('course/index.html', CourseIndex.as_view(), name='course_index'),

    # 专题列表
    path('course/list/<int:sub_id>.html', CourseList.as_view(), name='course_list'),

    # 专题详情
    path('course/detail/<int:art_id>.html', CourseDetailView.as_view(), name='course_detail'),

    # 未发布文章
    path('article/not/publish/list/<str:list_name>.html', NotPublishArticleListView.as_view(), name='not_publish_article_list'),
]





