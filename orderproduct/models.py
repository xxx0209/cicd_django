from django.db import models
from order.models import Order
from product.models import Product  # Product 앱에 있는 모델을 import

class OrderProduct(models.Model):
    id = models.BigAutoField(primary_key=True)

    # 주문과 다대일 관계
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_products'
    )

    # 상품과 다대일 관계
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_products'
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        db_table = 'order_products'
