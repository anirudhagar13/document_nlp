from . import views
from django.urls import path

app_name = 'DocProc'
urlpatterns = [
    path('', views.index, name='index'),
    path('echo/', views.echo, name='echo'),

]