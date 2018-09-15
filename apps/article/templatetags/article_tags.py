"""
article tags
"""
from article.models import *
from django import template
import time, datetime
from django.core.paginator import Paginator
from blog.settings import OWNER_NAME

register = template.Library()


######################################
# 获取所有者
######################################
@register.simple_tag
def get_owner_name():
    return OWNER_NAME


######################################
# 获取友情链接
######################################
@register.simple_tag
def get_friend_link():
    return FriendLink.objects.all()


######################################
# 获取热门文章
######################################
@register.simple_tag
def get_hot_article(num=5):
    return Article.objects.filter(is_publish=True).order_by('-views')[:num]


######################################
# 获取标签
######################################
@register.simple_tag
def get_tag():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)


######################################
# 获取最新评论
######################################
@register.simple_tag
def get_latest_comment(num=5):
    return Comment.objects.all().order_by('-add_time')[:num]


######################################
# 获取一年文章
######################################
@register.simple_tag
def get_all_article():
    # 获取当前年月
    year_now = datetime.datetime.now().year
    month_now = datetime.datetime.now().month

    # 判断年月份
    year = year_now - 1
    if month_now != 12:
        month = month_now + 1
    else:
        year = year + 1
        month = 1

    # 获取一年前时间节点
    year_ago = datetime.date(year, month, 1)
    return Article.objects.filter(add_time__gte=year_ago, is_publish=True).order_by('-add_time')


######################################
# 获取合作伙伴
######################################
@register.simple_tag
def get_partner():
    return Partner.objects.all()


######################################
# 获取上一篇
######################################
@register.simple_tag
def get_previous_article(art_id):
    art_id = int(art_id)
    previous_articles = Article.objects.filter(id__lt=art_id, is_publish=True)
    if previous_articles:
        previous_article = previous_articles.last()
        return previous_article
    else:
        return None


######################################
# 获取下一篇
######################################
@register.simple_tag
def get_next_article(art_id):
    art_id = int(art_id)
    next_articles = Article.objects.filter(id__gt=art_id, is_publish=True).order_by('-id')
    if next_articles:
        next_article = next_articles.last()
        return next_article
    else:
        return None


######################################
# 获取同类推荐
######################################
@register.simple_tag
def get_similar_article(art_id):
    art_id = int(art_id)
    cate = Article.objects.get(id=art_id).category
    similar_articles = Article.objects.filter(category=cate, is_publish=True).order_by('?')[:5]
    return similar_articles












