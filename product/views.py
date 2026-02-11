from django.shortcuts import render

from .models import Product

def product_carousel(request): # 상품 메인 페이지
    # 이미지 파일 이름에 "bigs" 포함된 상품만 필터링
    products = Product.objects.filter(image__icontains='bigs')

    return render(request, 'product/product_carousel.html', {'products': products})

# 상품 목록 조회 (필터/페이징)
from math import ceil

def product_list(request):
    # -----------------------
    # 🔍 GET 파라미터 처리
    # -----------------------
    page_number = int(request.GET.get('pageNumber', 0))
    page_size = int(request.GET.get('pageSize', 6))

    searchDateType = request.GET.get('searchDateType', 'all')
    category = request.GET.get('category', 'ALL')
    searchMode = request.GET.get('searchMode', 'ALL')
    searchKeyword = request.GET.get('searchKeyword', '')

    # -----------------------
    # 🔍 기본 상품 목록
    # -----------------------
    products = Product.objects.all().order_by('-id')

    # 카테고리 필터
    if category != "ALL":
        products = products.filter(category=category)

    # 검색 필터
    if searchKeyword:
        if searchMode == "name":
            products = products.filter(name__icontains=searchKeyword)
        elif searchMode == "description":
            products = products.filter(description__icontains=searchKeyword)
        else:
            products = products.filter(
                name__icontains=searchKeyword
            ) | products.filter(
                description__icontains=searchKeyword
            )

    # -----------------------
    # 📌 페이징 계산
    # -----------------------
    total_count = products.count()
    total_pages = ceil(total_count / page_size)

    start = page_number * page_size
    end = start + page_size
    paged_products = products[start:end]

    # 페이지 번호 리스트
    page_range = range(0, total_pages)

    # -----------------------
    # 📌 context 전달
    # -----------------------
    context = {
        "products": paged_products,
        "total": total_count,

        "page_number": page_number,
        "page_size": page_size,
        "total_pages": total_pages,
        "page_range": page_range,

        "category": category,
        "searchDateType": searchDateType,
        "searchMode": searchMode,
        "searchKeyword": searchKeyword,
    }

    return render(request, "product/product_list.html", context)

# 상품 상세 조회 (HTML 렌더링)
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return render(request, "product/product_not_found.html", status=404)

    context = {
        "product": product
    }
    return render(request, "product/product_detail.html", context)