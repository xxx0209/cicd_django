from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.create_order, name='create_order'),# 주문하기
    path('list/', views.order_list, name='order_list'),  # 특정 회원 주문 목록 조회
]
