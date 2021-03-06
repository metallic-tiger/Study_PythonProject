from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
import datetime
import json
import interface.crypt as crypt
from interface.taskManage import Send_active_Email
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
        user.password   = crypt.xor_encrypt(pwd,settings.SECRET_KEY)
        user.save()
        
        #发送邮件
        subject = '用户注册激活邮件'
        msg     = '用户激活邮件'
        sender  = settings.EMAIL_FROM
        rec     = [email]
        Tocker  = json.dumps({'datetime':datetime.datetime.now().strftime('%Y-%m-%d-%H'),'name' : name})
        html    = '<a>'+'127.0.0.1:8000' +'/user/on_live/'+crypt.xor_encrypt(Tocker,settings.SECRET_KEY)
        print(Tocker,'\n----\n',html)
                    
        Send_active_Email.delay(subject,msg,sender,rec,html)

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
        b_pwb = crypt.xor_encrypt(pwd,settings.SECRET_KEY)
        if a_pwd != b_pwb:
            print(name,' : pws err0!\n')
            return render(request,'login.html',{'errmsg':'密码错误'})
        
        #登录操作
        print(name,' : 登录成功!')
        #跳转页面
        return HttpResponseRedirect('/index')

#/user/on_live/<Tonker参数>
class on_live(View):
    def get(self,request,Token):
        print('step 0: ',Token)
        #激活验证----------
        #1.激活码编码检查
        
        try:
            Token = crypt.xor_decrypt(Token,settings.SECRET_KEY)
        except:
            print('非法参数')
            return render(request,'fail.html',{'fail':'step 1:非法的参数内容'})

        print('step 1: ',Token)
        #2. 激活码验证检查
        try:
            Token = Token.replace(settings.SECRET_KEY,"")#可以成功删减
            DeJson = json.loads(Token)#可以成功解析
        except:
            print('非法解析')
            return render(request,'fail.html',{'fail':'step 2:非法的解析内容'})

        date = datetime.datetime.strptime(DeJson['datetime'], '%Y-%m-%d-%H')
        name = DeJson['name']
        print('step 2: ',date,name)
        #3.激活码有效时间检查
        print(date)
        it = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d-%H'), '%Y-%m-%d-%H') - date
        hours, remainder = divmod(it.seconds, 3600)
        print(hours)
        if hours >2 :
            print(name,'过期')
            return render(request,'fail.html',{'fail':'step 3:激活时间过期'})

        try:
            user = models.User.objects.get(name = name)
            user.is_active = True
            user.save()
        except:
            print(name,'无此用户')
            return render(request,'fail.html',{'fail':'step 4:无此用户'})
        #激活成功-------------
        return render(request,'on_live.html',{'name':name})

    def post(self,request):
        return render(request,'fail.html',{'fail':'post - 非法的解析内容'})
        
        

        

    