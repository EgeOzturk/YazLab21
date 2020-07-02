from django.db import models

# Create your models here.

class UserBooks(models.Model):
    bookname = models.CharField(max_length=50,verbose_name="Kitap Adı")
    ISPN = models.CharField(max_length=13,verbose_name="ISPN Numarası")
    person = models.CharField(max_length=50,verbose_name="Alan Kişi Bilgisi")
    datetaken= models.DateTimeField(verbose_name="Alınan Tarih")
    duedate = models.DateTimeField(verbose_name="Teslim Tarihi")
    status = models.BooleanField(verbose_name="Geçikti mi?")

    def __str__(self):
        return self.bookname




