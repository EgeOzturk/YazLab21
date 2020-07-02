from django.contrib import admin
from django.urls import path

from . import views 

app_name="books"

urlpatterns = [
    path('addbook/',views.addbook,name="addbook"),
    path('listbooks/',views.listbooks,name="listbooks"),
    path('update/<int:id>',views.update,name="update"),
    path('delete/<int:id>',views.delete,name="delete"),
] 

