from django.db import models

# Create your models here.


class Books(models.Model):
    bookname = models.CharField(max_length=50,verbose_name="Kitap Adı")
    ISPN = models.CharField(max_length=13,verbose_name="ISPN Numarası")
    status = models.BooleanField(verbose_name="Mevcut mu?")
    image = models.FileField(verbose_name="Fotograf")

    def __str__(self):
        return self.bookname

