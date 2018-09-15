"""
article models
"""
from django.db import models
from django.db.models.aggregates import Count
import re


######################################
# 轮播图
######################################
class Banner(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    image = models.ImageField(verbose_name='轮播图', max_length=200, upload_to='banner/image/%Y/%m', help_text="970x250")
    url = models.CharField(verbose_name='链接', max_length=200)
    level = models.PositiveSmallIntegerField(verbose_name='级别', default=5, help_text='数字越小越靠前，默认5')
    target = models.PositiveSmallIntegerField(verbose_name='打开方式', choices=((1, '当前页'), (2, '新开页')), default=1)
    add_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


######################################
# 作者
######################################
class Author(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20, unique=True)
    qq = models.CharField(verbose_name='QQ', max_length=15, blank=True, null=True)
    mobile = models.CharField(verbose_name='手机', max_length=15, blank=True, null=True)
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 栏目分类
######################################
class Category(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20, unique=True)

    class Meta:
        verbose_name = '栏目分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 标签
######################################
class Tag(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20, unique=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 专题
######################################
class Subject(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20, unique=True)
    image = models.ImageField(verbose_name='封面', max_length=200, upload_to='article/subject/%Y/%m',
                              default='article/subject/default.png', help_text="350x170")
    banner_image = models.ImageField(verbose_name='大图', max_length=200, upload_to='article/subject/%Y/%m',
                              default='article/subject/default.png', help_text="970 x 250")
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '专题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 文章
######################################
class Article(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    author = models.ForeignKey(Author, verbose_name='作者', related_name='article_author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='栏目分类', related_name='article_category',
                                 on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    subject = models.ForeignKey(Subject, verbose_name='专题', related_name='article_subject', on_delete=models.CASCADE,
                                blank=True, null=True)
    image = models.ImageField(verbose_name='文章缩略图', max_length=200, upload_to='article/image/%Y/%m',
                              default='article/image/default.png', help_text="160x120")
    is_top = models.BooleanField(verbose_name='是否置顶', default=False)
    views = models.PositiveIntegerField(verbose_name='阅读量', default=0)
    content = models.TextField(verbose_name='正文')
    is_publish = models.BooleanField(verbose_name='是否发表', default=True)
    add_time = models.DateTimeField(verbose_name='发表时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s [ %s ]" % (self.title, self.author.name)

    # 每次调用该模型阅读量自加1
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 生成摘要
    def create_abstract(self):
        str1 = self.content
        p = re.compile('<[^>]+>')
        abstract = p.sub("", str1)
        abstract = abstract.replace('&nbsp;', '')[:100]
        return abstract


######################################
# 点赞
######################################
class Like(models.Model):
    article = models.ForeignKey(Article, verbose_name='文章', related_name='like_article', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='用户IP')
    add_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article.title


######################################
# 用户评论
######################################
class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='文章', related_name='comment_article', on_delete=models.CASCADE)
    user = models.PositiveSmallIntegerField(verbose_name='角色', choices=((1, '作者'), (2, '用户')), default=2)
    gender = models.PositiveSmallIntegerField(verbose_name='性别', choices=((1, '男'), (2, '女')), default=1)
    avatar = models.ImageField(verbose_name='头像', max_length=200, upload_to='img/avatar/%Y/%m',
                               default='img/avatar/default.png')
    comment = models.TextField(verbose_name='评论', max_length=200)
    ip = models.GenericIPAddressField(verbose_name='用户IP')
    address = models.CharField(verbose_name='地址', max_length=20)
    email = models.EmailField(verbose_name='邮箱')
    add_time = models.DateTimeField(verbose_name='发表时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[ %s ]: %s" % (self.article.title, self.comment)


######################################
# 评论回复
######################################
class CommentReplay(models.Model):
    comment = models.ForeignKey(Comment, verbose_name='评论', related_name='replay_comment', on_delete=models.CASCADE)
    replay = models.TextField(verbose_name='回复', max_length=200)
    user = models.PositiveSmallIntegerField(verbose_name='角色', choices=((1, '作者'), (2, '用户')), default=2)
    gender = models.PositiveSmallIntegerField(verbose_name='性别', choices=((1, '男'), (2, '女')), default=1)
    avatar = models.ImageField(verbose_name='头像', max_length=200, upload_to='img/avatar/%Y/%m',
                               default='img/avatar/default.png')
    ip = models.GenericIPAddressField(verbose_name='用户IP')
    address = models.CharField(verbose_name='地址', max_length=20)
    email = models.EmailField(verbose_name='邮箱')
    add_time = models.DateTimeField(verbose_name='发表时间', auto_now_add=True)

    class Meta:
        verbose_name = '回复评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[ %s ]: %s" % (self.comment.article.title, self.comment.comment)


######################################
# 友情链接
######################################
class FriendLink(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20, unique=True)
    url = models.CharField(verbose_name='链接', max_length=200, unique=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 合作伙伴
######################################
class Partner(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20, unique=True)
    url = models.CharField(verbose_name='链接', max_length=200, unique=True)

    class Meta:
        verbose_name = '合作伙伴'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
