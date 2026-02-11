from django.db import models

# 상품 카테고리 정보를 저장하기 위한 열거형 상수
# 영문 코드 + 한글 설명 구성
class Category(models.TextChoices):
    ALL = 'ALL', '전체'
    BREAD = 'BREAD', '빵'
    BEVERAGE = 'BEVERAGE', '음료수'
    CAKE = 'CAKE', '케이크'