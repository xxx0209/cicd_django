from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import Order
from product.models import Product
from orderproduct.models import OrderProduct

@login_required
@require_http_methods(["POST"])
def create_order(request):  # 주문하기 (POST)
    # 현재 로그인한 유저
    user = request.user

    # order_items 예시: ['1:2', '3:1'] → '상품ID:수량'
    order_items = request.POST.getlist('order_items')

    if not order_items:
        # 주문 상품이 없다면 주문 생성하지 않음
        return redirect('order:order_list')

    # 주문 생성
    order = Order.objects.create(
        member=user,
        status='PENDING',
        orderdate=timezone.now()
    )

    # 주문 상품 생성
    for item in order_items:
        product_id, quantity = map(int, item.split(':'))

        OrderProduct.objects.create(
            order=order,
            product_id=product_id,   # FK의 _id 필드를 직접 지정
            quantity=quantity
        )

        # 재고 차감
        product = Product.objects.get(id=product_id)
        product.stock -= quantity
        product.save()

    # 주문 생성 후 이동
    return redirect('order:order_list')

@login_required
def order_list(request): # 주문 목록 조회 (GET)
    user = request.user
    role = user.profile.role  # ADMIN 또는 USER

    if role == 'ADMIN':
        orders = Order.objects.all().order_by('-orderdate')
    else:
        orders = Order.objects.filter(member=user).order_by('-orderdate')

    context = {
        'orders': orders,
        'user_role': role,
    }
    return render(request, 'order/order_list.html', context)