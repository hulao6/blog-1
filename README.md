### Demo 地址
http://119.29.105.186:8080/

### 项目说明
1. 这是一个由 Django 2.0 + Python 3.5 开发的个人博客系统，出自己本身以外，用户无法登陆

2. 用户评论采用获取其客户端 IP 地址进行判断其所属地区

3. 用户评论只能到 2 级评论

4. 博主写文章需要后台先登录管理员账户，然后回收主页就可以看到右上角有了其它的一些按钮

5. 写博客时，标签，专题，作者等都需要在后台预先定义

6. 首页轮播图需要在后台添加，且有一张图的优先级必须是1，否则无法显示

7. 合作伙伴，友链均可在后台添加

8. 右边的小按钮图片则需要自己去指定目录修改相应的图片和信息

9. 博客的所属标题在settings.py 里面进行配置

### 部署方式

1. 部署和平台的 django 一样，先建立环境，推荐使用 virtualenv，参照 require 文件安装相应版本，否则可能出现不兼容

2. 同步数据库和创建超级管理员

3. 登录后台进行简单的初始化操作，注意这里的后台地址为了安全已经不再是 /admin，具体可以去查看代码

### 示例图片

![enter description here](https://github.com/PythonTra1nee/blog/blob/master/display/index.png?raw=true)

![enter description here](https://github.com/PythonTra1nee/blog/blob/master/display/detail.png?raw=true)

![enter description here](https://github.com/PythonTra1nee/blog/blob/master/display/course.png?raw=true)
