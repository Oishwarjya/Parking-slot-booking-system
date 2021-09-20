from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('login/', views.index, name='Parking slot booking Login'),
    #path('admin/', admin.site.urls),
    #path('', include('mainapp.urls')),
    #path('', views.home, name='PropertyManager Home'),
]