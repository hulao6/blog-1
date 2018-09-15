"""
article views Configuration
"""
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse, Http404
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from pure_pagination import PageNotAnInteger, Paginator
import json, datetime, urllib, time, random
from django.views.decorators.csrf import csrf_protect

from utils.users import LoginCheck, GetIPLocation
from .models import *
from .forms import *
from blog.settings import SERVICE_URL


######################################
# 首页
######################################
class IndexView(View):
    def get(self, request):
        menu_name = 'index'

        # 获取轮播图
        banners = Banner.objects.all().order_by('level')

        # 获取置顶文章
        top_articles = Article.objects.filter(is_top=True, is_publish=True)

        # 获取其它文章
        normal_articles = Article.objects.filter(is_top=False, is_publish=True).order_by('-add_time')

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(normal_articles, 10, request=request)

        # 分页处理后的 QuerySet
        normal_articles = p.page(page)

        context = {
            'menu_name': menu_name,
            'banners': banners,
            'top_articles': top_articles,
            'normal_articles': normal_articles,
        }

        return render(request, 'article/index.html', context=context)


######################################
# 写文章
######################################
class WriteArticleView(LoginCheck, View):
    def get(self, request):
        menu_name = 'article_write'

        # 获取作者
        authors = Author.objects.all()

        # 获取标签
        tags = Tag.objects.all()

        # 获取栏目
        categorys = Category.objects.all()

        # 获取专题
        subjects = Subject.objects.all()

        context = {
            'menu_name': menu_name,
            'authors': authors,
            'tags': tags,
            'categorys': categorys,
            'subjects': subjects,
        }

        return render(request, 'article/write.html', context=context)

    def post(self, request):
        add_article_form = AddArticleForm(request.POST)
        if add_article_form.is_valid():
            article = Article()
            article.title = request.POST.get('title')
            article.author_id = int(request.POST.get('author'))

            # 获取分类
            category_id = int(request.POST.get('category'))
            category_name = Category.objects.get(id=category_id).name

            article.category_id = category_id

            # 判断是否有专题
            subject = request.POST.get('subject', '')
            if subject != '':
                article.subject_id = int(subject)

            # 安装分类设置默认缩略图
            if category_name == '运维':
                article.image = 'article/image/yw_default.png'
            elif category_name == '开发':
                article.image = 'article/image/dev_default.png'
            elif category_name == '随笔':
                article.image = 'article/image/sb_default.png'
            else:
                article.image = 'article/image/default.png'

            # 判断置顶
            if int(request.POST.get('is_top')) == 1:
                article.is_top = True
            else:
                article.is_top = False

            content = request.POST.get('content', "")
            if content != "":
                article.content = content
            else:
                return HttpResponse('{"status":"failed", "msg":"内容不能为空！"}', content_type='application/json')

            tag_list = request.POST.getlist('tag')

            if len(tag_list) == 0:
                return HttpResponse('{"status":"failed", "msg":"标签不能为空！"}', content_type='application/json')

            article.is_publish = False

            article.save()

            for each in request.POST.getlist('tag'):
                article.tag.add(int(each))
                article.save()

            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failed", "msg":"未知错误！"}', content_type='application/json')


######################################
# 文章详情
######################################
class DetailView(View):
    def get(self, request, art_id):
        article = Article.objects.get(id=art_id)

        # 判断栏目
        if article.category.name == '运维':
            menu_name = 'oprations'
        elif article.category.name == '开发':
            menu_name = 'develops'
        else:
            menu_name = 'essay'

        # 判断是否点赞
        ip = request.META['REMOTE_ADDR']
        is_like = Like.objects.filter(ip=ip, article_id=art_id)

        # 阅读量
        article.increase_views()

        # 评论
        comments = Comment.objects.filter(article_id=art_id)

        # 评论判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(comments, 5, request=request)

        # 分页处理后的 QuerySet
        comments = p.page(page)

        context = {
            'article': article,
            'menu_name': menu_name,
            'is_like': is_like,
            'SERVICE_URL': SERVICE_URL,
            'comments': comments,
        }

        return render(request, 'article/detail.html', context=context)


######################################
# 文章点赞
######################################
class ArticleLikeView(View):
    def post(self, request):
        art_id = int(request.POST.get('art_id'))
        ip = request.META['REMOTE_ADDR']
        try:
            like = Like()
            like.article_id = art_id
            like.ip = ip
            like.save()
            return HttpResponse('{"status":"success", "msg":"点赞成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"未知错误！"}', content_type='application/json')


######################################
# 文章评论
######################################
class ArticleCommentView(View):
    def post(self, request):
        add_comment_form = AddArticleCommentForm(request.POST)
        if add_comment_form.is_valid():
            try:
                user = int(request.POST.get('user'))
                email = request.POST.get('email')
                comment = request.POST.get('comment')
                if user == 1:
                    ip = '127.0.0.1'
                    address = '深圳'
                    gender = 1
                    avatar = 'img/avatar/default.png'
                else:
                    ip = request.META['REMOTE_ADDR']
                    address = GetIPLocation(ip)
                    gender = int(request.POST.get('gender'))

                    # 根据性别随机头像
                    random_num = random.randint(1, 5)
                    if gender == 1:
                        avatar = 'img/avatar/man_' + str(random_num) + '.png'
                    else:
                        avatar = 'img/avatar/woman_' + str(random_num) + '.png'

                # 判断是评论还是回复
                cmt_id = request.POST.get('cmt_id', '')

                if cmt_id == '':
                    art_id = int(request.POST.get('art_id'))
                    cmt = Comment()
                    cmt.article_id = art_id
                    cmt.user = user
                    cmt.gender = gender
                    cmt.avatar = avatar
                    cmt.comment = comment
                    cmt.ip = ip
                    cmt.address = address
                    cmt.email = email
                    cmt.save()
                    return HttpResponse('{"status":"success", "msg":"评论成功！"}', content_type='application/json')
                else:
                    cmt_rep = CommentReplay()
                    cmt_rep.comment_id = int(cmt_id)
                    cmt_rep.replay = comment
                    cmt_rep.user = user
                    cmt_rep.gender = gender
                    cmt_rep.avatar = avatar
                    cmt_rep.ip = ip
                    cmt_rep.address = address
                    cmt_rep.email = email
                    cmt_rep.save()
                    return HttpResponse('{"status":"success", "msg":"回复成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"failed", "msg":"评论失败！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failed", "msg":"填写不合法！"}', content_type='application/json')


######################################
# CKEDITOR 上传图片
######################################
@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        callback = request.GET.get('CKEditorFuncNum')
        try:
            # path 修改上传的路径
            path = "media/article/ckeditor/image/" + time.strftime("%Y%m%d%H%M%S", time.localtime())
            f = request.FILES["upload"]
            file_name = path + "_" + f.name
            des_origin_f = open(file_name, "wb+")
            # 直接遍历类文件类型就可以生成迭代器了
            for chunk in f:
                des_origin_f.write(chunk)
            des_origin_f.close()
        except Exception as e:
            print(e)
        res = r"<script>window.parent.CKEDITOR.tools.callFunction(" + callback + ",'/" + file_name + "', '');</script>"
        return HttpResponse(res)
    else:
        raise Http404()


######################################
# 文章列表
######################################
class ArticleListView(View):
    def get(self, request, list_name):
        if list_name != 'other':
            if list_name == 'oprations':
                menu_name = 'oprations'
                list_title = '运维文章列表'
                cate = Category.objects.get(name='运维')
            elif list_name == 'develops':
                menu_name = 'develops'
                list_title = '开发文章列表'
                cate = Category.objects.get(name='开发')
            else:
                menu_name = 'essay'
                list_title = '随笔文章列表'
                cate = Category.objects.get(name='随笔')

            # 获取文章
            normal_articles = Article.objects.filter(category=cate, is_publish=True).order_by('-add_time')
        else:
            menu_name = 'other'

            # 归档
            year = request.GET.get('year', '')
            month = request.GET.get('month', '')
            if (year != ''):
                list_title = '%s 年文章归档' % year
                normal_articles = Article.objects.filter(add_time__year=year, is_publish=True).order_by('-add_time')

                if (month != ''):
                    list_title = '%s 年 %s 月文章归档' % (year, month)
                    normal_articles = Article.objects.filter(add_time__month=month)

            # 标签
            tag = request.GET.get('tag', '')
            if tag != '':
                list_title = '标签为 "%s" 的文章' % tag
                normal_articles = Article.objects.filter(tag__name=tag, is_publish=True)

            # 搜索
            keyword = request.GET.get('keyword', '')
            if keyword != '':
                list_title = '关键词 "%s" 的搜索结果' % keyword
                normal_articles = Article.objects.filter(
                    Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(tag__name__icontains=keyword) | Q(
                        category__name__icontains=keyword) | Q(author__name__icontains=keyword)).filter(is_publish=True)

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(normal_articles, 10, request=request)

        # 分页处理后的 QuerySet
        normal_articles = p.page(page)

        context = {
            'menu_name': menu_name,
            'list_title': list_title,
            'normal_articles': normal_articles,
        }

        return render(request, 'article/list.html', context=context)


######################################
# 专题首页
######################################
class CourseIndex(View):
    def get(self, request):
        menu_name = 'course'

        courses = Subject.objects.all().order_by('-add_time')

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(courses, 9, request=request)

        # 分页处理后的 QuerySet
        courses = p.page(page)

        context = {
            'menu_name': menu_name,
            'courses': courses,
        }

        return render(request, 'article/course_index.html', context=context)


######################################
# 专题列表
######################################
class CourseList(View):
    def get(self, request, sub_id):
        menu_name = 'course'

        course = Subject.objects.get(id=int(sub_id))

        # 专题
        all_course = Article.objects.filter(subject_id=int(sub_id), is_publish=True)

        articles = Article.objects.filter(subject_id=int(sub_id), is_publish=True).order_by('-add_time')

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(articles, 10, request=request)

        # 分页处理后的 QuerySet
        articles = p.page(page)

        context = {
            'menu_name': menu_name,
            'course': course,
            'all_course': all_course,
            'articles': articles,
        }

        return render(request, 'article/course_list.html', context=context)


######################################
# 专题文章详情
######################################
class CourseDetailView(View):
    def get(self, request, art_id):
        article = Article.objects.get(id=art_id)

        # 专题
        all_course = Article.objects.filter(subject_id=article.subject_id, is_publish=True)

        menu_name = 'course'

        # 判断是否点赞
        ip = request.META['REMOTE_ADDR']
        is_like = Like.objects.filter(ip=ip, article_id=art_id)

        # 阅读量
        article.increase_views()

        # 评论
        comments = Comment.objects.filter(article_id=art_id)

        # 评论判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(comments, 5, request=request)

        # 分页处理后的 QuerySet
        comments = p.page(page)

        context = {
            'article': article,
            'all_course': all_course,
            'menu_name': menu_name,
            'is_like': is_like,
            'SERVICE_URL': SERVICE_URL,
            'comments': comments,
        }

        return render(request, 'article/course_detail.html', context=context)


######################################
# 未发布文章列表
######################################
class NotPublishArticleListView(View, LoginCheck):
    def get(self, request, list_name):
        menu_name = list_name
        list_title = '未发布文章'

        normal_articles = Article.objects.filter(is_publish=False)

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(normal_articles, 10, request=request)

        # 分页处理后的 QuerySet
        normal_articles = p.page(page)

        context = {
            'menu_name': menu_name,
            'list_title': list_title,
            'normal_articles': normal_articles,
        }

        return render(request, 'article/list.html', context=context)
