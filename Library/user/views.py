from django.shortcuts import render, HttpResponse,redirect

from .forms import RegisterForm,LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from datetime import date

from .models import Users
from borrowbook.models import UserBooks
from books.models import Books

# Create your views here.

def Control():
    listBorrowBooks = UserBooks.objects.filter(Q(status=False))
    for i in listBorrowBooks:
        if str(i.duedate) < str(date.today()):
            UserBooks.objects.filter(duedate=i.duedate).update(status=True)
    

def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")   # aynı ise şifre ve kullanıcı adı bilgiler alınıyor
        password = form.cleaned_data.get("password")
        superuser = form.cleaned_data.get("superuser")

        userlogin = User(username=username)
        userlogin.set_password(password)
        userlogin.is_superuser = superuser
        userlogin.save()

        newUser = Users(username=username,superuser=superuser)
        newUser.save()
        
        login(request,userlogin)

        messages.success(request,"Başarılı Bir Şekilde Kayıt Oldunuz...")
        
        Control()                                                        #Borrow Books date Upgared

        return redirect("index")

    context = {
        "form" : form
    }

    return render(request,"register.html",context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form 
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username,password=password)

        if user is None:
            messages.info(request,"Kullanıcı Adı Veya Paralo Hatalı!!!")
            return render(request,"login.html",context)

        messages.success(request,"Başarıyla Giriş Yaptınız!!!")
        login(request,user) 
        
        Control()                                                 #Borrow Books date Upgared
        
        return redirect("index")  

    return render(request,"login.html",context)  

@login_required(login_url="user:login")
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız!!!")
    return redirect("index")    

@login_required(login_url="user:login")
def listuser(request,id):

    keyword = request.GET.get('keyword')

    if keyword:
        listuser =  Users.objects.filter(username=keyword)
        context = {
            "listuser":listuser
        }
        return render(request,"listuser.html",context)

    listuser =  Users.objects.filter()
    usr = Users.objects.get(id=id)
    name = usr.username
    context = {
        "listuser":listuser,
        "name":name
    }
    
    return render(request,"listuser.html",context)

@login_required(login_url="user:login")
def delete(request,id):
    
    name = Users.objects.get(id=id)
    
    control = UserBooks.objects.all()
    for ctr in control:
        if ctr.person == name.username:
            messages.info(request,"Bu Kullanıcıyı Üzerindeki Kitabı Getirmeden Sillemezsiniz.")  
            return listuser(request,id)                    
        
    User.objects.filter(id=id).delete()
    Users.objects.filter(id=id).delete()

    return listuser(request,id)






