from django.db import models
from django.conf import settings
from django.utils import timezone

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', '대기'
        COMPLETED = 'COMPLETED', '완료'
        CANCELED = 'CANCELED', '취소'

    id = models.BigAutoField(primary_key=True)

    # 회원 1명이 여러 주문 가능
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 기본 User 모델
        on_delete=models.CASCADE,
        related_name='orders'
    )

    orderdate = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    def __str__(self):
        return f"Order {self.id} ({self.status})"

    class Meta:
        db_table = 'orders'  # 스프링과 동일한 테이블명
