from django.contrib import admin
from django.urls import path

from . import views 

app_name="borrowbook"

urlpatterns = [
    path('list/',views.list,name="list"),
    path('timelapse/',views.timelapse,name="timelapse"),
    path('takenbookview/',views.takenbookview,name="takenbookview"),
    path('givebook/<person>/',views.givebook,name="givebook"),
    path('yourbooks/<person>/',views.yourbooks,name="yourbooks"),
    path('takenbook/<int:id>/<int:userId>/',views.takenbook,name="takenbook"),
    path('time/<int:bookId>/',views.time,name="time"),
    path('time/everybody/',views.everbody,name="everbody")
] 

