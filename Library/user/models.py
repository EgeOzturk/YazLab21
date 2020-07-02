from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=60,verbose_name="Kullanıcı Adı")
    superuser = models.BooleanField(verbose_name="Admin")

    def __str__(self):
        return self.username







