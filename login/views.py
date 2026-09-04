from django.shortcuts import render,redirect
from .import models
# Create your views here.


# 設定Index,原有的是login.html,改成index.html (2025-0728)
def index(request):
    return render(request, 'index.html')

# def index(request):
#     return render(request, 'login/index.html')


def login(request):
    if request.session.get('loginFlag'):
        return redirect('/')

    if request.method == "POST":
       email = request.POST.get("email",None)
       print(email)
       pwd= request.POST.get("password",None)
       if email and pwd:
           user = models.User.objects.filter(email=email)
           print(user)
           if user:
               _pwd=user[0].pwd
               print(_pwd)
           else:
            return render(request, 'login/login.html')
           if pwd ==_pwd: 
                request.session['loginFlag']= True
                request.session['username']= user[0].name
                return redirect('/')
           else:
                
                return render(request, 'login/login.html',)
    return render(request, 'login/login.html')
    
    


def register(request):
   if request.method == "POST":
       email = request.POST.get("email",None)
       name= request.POST.get("name",None)
       pwd1= request.POST.get("password1",None)
       pwd2= request.POST.get("password2",None)
       if pwd1 == pwd2:
           user=models.User.objects.filter(email=email)
           if user:
               print('帳戶已經被註冊, 請重新註冊 Already Existed, Plz register again')
               return redirect("/register/")
           new_user = models.User.objects.create()
           new_user.email = email
           new_user.name= name
           new_user.pwd = pwd1
           new_user.save()
           return redirect('/login/')
       
       
   
   return render(request, 'login/register.html')

def logout(request):
    if request.session.get('loginFlag', None):
        request.session.flush()
        return redirect('/')

    return redirect('/')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # 假設你用自己的方法驗證使用者
        user = authenticate(username=username, password=password)  # 或你的驗證函式
        if user is not None:
            # 驗證成功，設定 session
            request.session['loginFlag'] = True
            request.session['username'] = user.username  # 或你要用的名稱

            # 可能跳轉到首頁或其他頁面
            return redirect('/')
        else:
            # 驗證失敗，回傳錯誤訊息
            return render(request, "login.html", {"error": "帳號或密碼錯誤"})
    else:
        return render(request, "login.html")

import os


def ai_assistant(request):
    from google import genai

    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents="請幫我分析這筆登入紀錄..."
    )
    return response.text
