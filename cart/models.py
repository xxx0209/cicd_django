from django.db import models
from django.conf import settings

# OneToOneField
# 한 명의 유저는 단 하나의 Cart만 가질 수 있음
# 한 개의 Cart는 정확히 한 명의 유저에게만 속함
# 즉 1:1 관계를 만듦

# Member 모델은 일반적으로 User 모델을 쓰거나 커스텀 User 모델을 사용할 수 있습니다.
# settings.AUTH_USER_MODEL : Django의 User 모델입니다.
# related_name 속성이 없으면 cart_set처럼 이름이 자동으로 생성되는데
# OneToOneField에서는 user.cart 와 같이 명확한 속성명이 더 좋습니다.
class Cart(models.Model):
    member = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    class Meta:
        db_table = "carts"

    def __str__(self):
        return f"Cart(id={self.id}, member={self.member.username})"
