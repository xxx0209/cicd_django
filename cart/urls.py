from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('insert/', views.add_to_cart, name='add_to_cart'),
    path('list/<int:member_id>/', views.cart_list, name='cart_list'),
]
