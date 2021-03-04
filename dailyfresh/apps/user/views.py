from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
import datetime
import json
import base64
import re

from user import models
#/user/register
class Register(View):
    def get(self,request):
        return render(request,'register.html',{'errmsg':''})
    def post(self,request):
        '注册处理'
        #接受数据
        name = request.POST.get('user_name')
        pwd  = request.POST.get('pwd')
        email= request.POST.get('email')
        allow= request.POST.get('allow')
        #数据校验
        try:
            userif = models.User.objects.get(username= name)
        except:
            userif = None
        if userif :
            return render(request ,'register.html',{'errmsg':'用户名已存在'})

        if not all([name,pwd,email,allow]):
            #数据不完整
            print('用户注册-数据不完整')
            return render(request ,'register.html',{'errmsg':'数据不完整'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            #邮箱不合法
            return render(request ,'register.html',{'errmsg':'邮箱不合法'})
        
        if  20<pwd.__len__() or pwd.__len__()<8 or re.search('[^\w]',pwd):
            #密码最少8位,最长20位
            print('密码最少8位,最长20位')
            return render(request ,'register.html',{'errmsg':'密码最少8位,最长20位,且不能有特殊字符'})
        
        if not allow=='on' : 
            #没有同意协议
            return render(request ,'register.html',{'errmsg':'没有同意协议'}) 
        #业务处理
        user            = models.User()
        user.email      = email
        user.username   = name
        user.is_active  = False
        #加密后存入 数据库
        user.password   = base64.b64encode(bytes(pwd+settings.SECRET_KEY,'ascii')).decode('utf-8')
        user.save()
        
        #发送邮件
        subject = '用户注册激活邮件'
        msg     = '用户激活邮件'
        sender  = settings.EMAIL_FROM
        rec     = [email]
        Tocker  = json.dumps({'datetime':datetime.datetime.now().hour,'name' = name})
        html    = '<a>'+settings.Localhost +'/user/on_live?Tonker'+

        send_mail(subject,msg,sender,rec,html_message=)

        #应答
        return HttpResponseRedirect('/index')
#/user/login
class Login(View):
    def get(self,request):
        return render(request,'login.html',{'errmsg':''})
    
    def post(self,request):
        #获取数据
        name = request.POST.get('username')
        pwd  = request.POST.get('pwd')

        #验证用户
        try:
            User = models.User.objects.get(username= name)
        except:
            print(name,' : 登录fail!')
            return render(request,'login.html',{'errmsg':'无此用户'})

        a_pwd = User.password
        b_pwb = base64.b64encode(bytes(pwd+settings.SECRET_KEY,'ascii')).decode('utf-8')
        if a_pwd != b_pwb:
            print(name,' : pws err0!\n')
            return render(request,'login.html',{'errmsg':'密码错误'})
        
        #登录操作
        print(name,' : 登录成功!')
        #跳转页面
        return HttpResponseRedirect('/index')

class on_live(View):
    def get(self,request,Token):
        
        return render(request ,'register.html',{'name':username})

    def post(self,request):
        
        

        

    