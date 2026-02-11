from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from product.models import Product
from cartproduct.models import CartProduct
from .models import Cart

@require_POST
def add_to_cart(request): # 장바구니에 상품 담기
    """
    장바구니에 상품 추가 후, 상품 목록 페이지로 이동
    """
    member_id = request.user.id  # 로그인한 회원
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(member_id=member_id)

    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_product.quantity += quantity # 이미 담겨 있는 상품 개수 누적
        cart_product.save()

    # 성공 메시지 생성
    messages.success(request, f"장바구니에 상품 '{product.name}'가 {quantity}개 추가되었습니다.")

    # 상품 목록 페이지로 이동
    return redirect('product:product_list')  # urls.py에 설정한 이름

@login_required # 특정 회원의 장바구니 상품 조회
def cart_list(request, member_id):
    """
    특정 회원의 장바구니 상품 조회 후 HTML로 렌더링
    """
    try:
        cart = get_object_or_404(Cart, member_id=member_id)
        cart_items = CartProduct.objects.filter(cart=cart).select_related('product')

        # 장바구니 총 금액과 각 항목 금액 계산
        cart_total_price = 0
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            cart_total_price += item.total_price

        context = {
            'cart_products': cart_items,
            'cart_total_price': cart_total_price,
        }

    except Cart.DoesNotExist:
        context = {
            'cart_products': [],
            'cart_total_price': 0,
        }

    return render(request, 'cart/cart_list.html', context)
