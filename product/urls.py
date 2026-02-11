from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('list/', views.product_list, name='product_list'),
    path('detail/<int:id>/', views.product_detail, name='detail'),
]
