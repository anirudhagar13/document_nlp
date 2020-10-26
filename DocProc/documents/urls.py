from . import views
from django.urls import path

app_name = 'DocProc'
urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('train/', views.train, name='train')

]