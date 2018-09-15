"""
User functions
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import urllib, json


######################################
# 用户是否登录检测
######################################
class LoginCheck(object):
    @method_decorator(login_required(login_url='/admin4blog/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginCheck, self).dispatch(request, *args, **kwargs)


######################################
# 获取地区
######################################
def GetIPLocation(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip="
    data = urllib.request.urlopen(url + ip).read().decode("utf-8")
    datadict=json.loads(data)

    for oneinfo in datadict:
        if "code" == oneinfo:
            if datadict[oneinfo] == 0:
                county = datadict["data"]["county"]
                if county != '内网IP':
                    # country = datadict["data"]["country"]
                    # provience = datadict["data"]["region"]
                    city = datadict["data"]["city"]
                    address = city
                else:
                    address = '未知'
                return address

















