from django.urls import path
from . import views

app_name = 'minitest'

urlpatterns = [
    path('fruit/', views.fruit, name='fruit'),
    path('fruit/list/', views.fruit_list, name='fruit_list'),
]
