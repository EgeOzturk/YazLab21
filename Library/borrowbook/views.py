from django.shortcuts import HttpResponse, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from datetime import date
from _datetime import timedelta

from .models import UserBooks
from books.models import Books
from user.models import Users
from Library.tesseract import Tesseract as ts

# Create your views here.

def index(request):
    return render(request,"index.html")

@login_required(login_url="user:login")
def list(request):                                #Admin için hangi kitapların ne zaman teslim edileceği ekranı getirir 
    listuserbooks =  UserBooks.objects.all()
    context = {
        "listuserbooks":listuserbooks
    }
    return render(request,"list.html",context)

@login_required(login_url="user:login")
def timelapse(request):                           #Admin için zaman atlama methodu
    listuserbooks =  UserBooks.objects.all()
    control = 1
    context = {
        "listuserbooks":listuserbooks,
        "control":control
    }
    return render(request,"list.html",context)

@login_required(login_url="user:login")
def takenbookview(request):               #Alınabilecek kitapları gösterir normal kullanıcılar için
    
    keyword = request.GET.get("keyword")
    control = 1
    
    if keyword:
        listbook = Books.objects.filter((Q(bookname__contains=keyword)|Q(ISPN__contains=keyword))&Q(status__contains=1))
        
        context = {
            "listbook":listbook,
            "control":control
        }
        return render(request,"listbooks.html",context)

    listbook =  Books.objects.filter(Q(status__contains=1))    # 1 = True 0 = False  
    return render(request,"listbooks.html", {"listbook":listbook,"control":control})

@login_required(login_url="user:login")
def givebook(request,person):
    
    control = UserBooks.objects.filter(Q(person=person)) 

    if control:
        if request.method == 'POST' and request.FILES['image']:
            
            image = request.FILES['image']
            fs = FileSystemStorage()
            imgPath = fs.save(image.name, image)
            uploadImg = fs.url(imgPath)
            
            ISPN = ts().handle_ISBNs(image)    #tesseract
           
            if ISPN == "Bulunamadı": 
                messages.error(request,"Üzgünüz, ISPN Numarası Bulunamadığı İçin Geri Teslim İşlemi Yapılamadı.")
                return render(request,"givenbook.html",{'uploadImg':uploadImg})   
            
            if UserBooks.objects.filter(Q(person=person,ISPN=ISPN)):
            
                usrBookDelete = get_object_or_404(UserBooks,ISPN=ISPN,person=person) 
                usrBookDelete.delete()
            
                book = Books.objects.filter(Q(ISPN=ISPN)).update(status=1) 
                book = Books.objects.get(ISPN=ISPN)
                bookname = book.bookname

                messages.success(request,"Kitabı Başarılı Bir Şekilde Teslim Ettiniz.")
                ispn = ISPN[0] + '-' + ISPN[1:7] + '-' +  ISPN[7:] 
                return render(request,'givenbook.html',{'uploadImg':uploadImg, 'ISPN':ispn, 'bookname':bookname})

            messages.error(request,"Üzgünüz, ISPN Numarası Yanlış Bulundu.Başka Bir Fotograf Deneyiniz.")
            return render(request,'givenbook.html',{'uploadImg':uploadImg,'ISPN':ISPN})
    else:
        messages.warning(request,"Teslim Edilebilecek Kitap Bulunamamıştır.")
        return takenbookview(request)
            
    return render(request,'givenbook.html')

@login_required(login_url="user:login")
def yourbooks(request,person):                           #Kişini aldığı kitapları gösterir (o an üzerinde olduğu)
    listuserbooks =  UserBooks.objects.filter(Q(person__contains=person))
    context = {
        "listuserbooks":listuserbooks
    }
    return render(request,"list.html",context)

@login_required(login_url="user:login")
def takenbook(request,id,userId):                      #sql'e kullanıcının aldığı kitabın bilgisini ekleme methodu 

    userbooks = UserBooks.objects.all()
    user = Users.objects.get(id=userId)
    ctl = 0
    for bookNum in userbooks:
        if bookNum.person == user.username:
            ctl += 1
            if bookNum.status == 1:
                messages.error(request,"Üzgünüz, Teslim Tarihi Geçmiş Kitabınızı Teslim Etmeden Yeni Kitap Alamazsınız.")
                return takenbookview(request)            
    if ctl >= 3:
        messages.error(request,"Üzgünüz, Daha Fazla Kitap Alamazsınız...")
        return takenbookview(request)

    bookStatus = Books.objects.filter(id=id).update(status=0)
    book = Books.objects.get(id=id)
    tDate = date.today()
    dDate = tDate + timedelta(days=7)
    yourbook = UserBooks(id=id,bookname=book.bookname,ISPN=book.ISPN,person=user.username,datetaken=tDate,duedate=dDate,status=0)
    yourbook.save()
    
    listuserbooks = UserBooks.objects.filter(Q(id__contains=id))
    context = {
        "listuserbooks":listuserbooks
    }

    messages.success(request,"Kitabı Başarlı Bir Şekilde Ödünç Aldınız...")

    return render(request,"list.html",context)

def time(request,bookId):

    try:
        keyword = int(request.GET.get('keyword'))
    except :
        messages.info(request,"Lütfen Sayı Giriniz...")
        return timelapse(request)    

    if keyword:
        borrowB = UserBooks.objects.get(id=bookId)
        newDate = borrowB.datetaken + timedelta(days=keyword)

        if newDate > borrowB.duedate:
            borrowB = UserBooks.objects.filter(id=bookId).update(datetaken=newDate,status=1)
        else:
            if keyword < 0 :
                borrowB = UserBooks.objects.filter(id=bookId).update(datetaken=newDate,status=0)
            borrowB = UserBooks.objects.filter(id=bookId).update(datetaken=newDate)

        messages.success(request,"Öteleme İşlemi Başarılı Bir Şekilde Gerçekleştirildi.")

        return timelapse(request)      

def everbody(request):
    try:
        keyword = int(request.GET.get('keyword2'))
    except :
        messages.info(request,"Lütfen Sayı Giriniz...")
        return timelapse(request)  

    if keyword:
        borrowB = UserBooks.objects.all()

        for books in borrowB:
            newDate = books.datetaken + timedelta(days=keyword)
            
            if newDate > books.duedate:
                UserBooks.objects.filter(id=books.id).update(datetaken=newDate,status=1)
            else:
                if keyword < 0 :
                    UserBooks.objects.filter(id=books.id).update(datetaken=newDate,status=0)
                UserBooks.objects.filter(id=books.id).update(datetaken=newDate)
           
        messages.success(request,"Öteleme İşlemi Başarılı Bir Şekilde Tüm Kullanıcılar İçin Gerçekleştirildi.")    
        
        return timelapse(request)   




