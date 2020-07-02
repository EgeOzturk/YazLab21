from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import AddBook
from .models import Books
from Library.tesseract import Tesseract as ts

# Create your views here.


def index(request):
    return render(request,"index.html")

@login_required(login_url="user:login")
def addbook(request):
    
    form = AddBook(request.POST or None,request.FILES or None)

    context = {
        "form":form 
    }
    
    if form.is_valid():
        bookname = form.cleaned_data.get("bookname")   
        image = form.cleaned_data.get("image")

        if image:
            ISPN = ts().handle_ISBNs(image)   
            if ISPN == "Bulunamadı":
                messages.error(request,"Üzgünüz, ISPN Numarası Bulunamadığı İçin Kayıt İşlemi Yapılamadı.")
                return render(request,"addbook.html",context)
        
        controlISPN = Books.objects.filter(Q(ISPN=ISPN))
        if controlISPN:
            messages.error(request,"Kitap Zaten Kayıtlı.")
            return render(request,"addbook.html",context)
    
        newBook = Books(bookname=bookname,ISPN=ISPN,status=1,image=image)
        newBook.save()  

        messages.success(request,"Kitap Başarılı Bir Şekilde Kaydedildi...")

        return render(request,"addbook.html",{'form':form, 'newBook' : newBook})
        

    return render(request,"addbook.html",context)

@login_required(login_url="user:login")
def listbooks(request):
   
    keyword = request.GET.get("keyword")
   
    if keyword:
        listbook = Books.objects.filter(Q(bookname__contains=keyword)|Q(ISPN__contains=keyword))
        context = {
            "listbook":listbook
        }
        return render(request,"listbooks.html",context)

    listbook =  Books.objects.all()
    return render(request,"listbooks.html", {"listbook":listbook})

@login_required(login_url="user:login")
def update(request,id):
    
    control = Books.objects.get(id=id)
    if control.status == 0:
        messages.info(request,"Bu Kitabı Şuan Güncelleyemezsiniz.")
        return listbooks(request)

    keyword = request.GET.get("keywordName")
    if keyword:
        Books.objects.filter(id=id).update(bookname=keyword)
        messages.success(request,"Kitap İsmi Başarıyla Güncellendi.")
        return listbooks(request)
   
    updateBook = 5
    listbook =  Books.objects.all()
    return render(request,"listbooks.html",{"listbook":listbook,"updateBook":updateBook})

@login_required(login_url="user:login")
def delete(request,id):
    
    control = Books.objects.get(id=id)
    if control.status == 0:
        messages.info(request,"Bu Kitabı Şuan Silemezsiniz.")
        return listbooks(request)

    Books.objects.filter(id=id).delete()
    messages.success(request,"Kitap Başarılı Bir Şekilde Silindi.")
    return listbooks(request)
