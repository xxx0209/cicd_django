from django.db import models
from cart.models import Cart

# Cart : 한 회원의 장바구니
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')

    # Product 모델은 다른 앱(product)에 있으므로 앱 이름을 포함시켜 주어야 합니다.
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_products"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
