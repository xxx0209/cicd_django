from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from product.Category import Category

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.IntegerField(validators=[MinValueValidator(100)], null=False)
    category = models.CharField(max_length=20, choices=Category.choices, null=False)
    stock = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(1000)], null=False)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField(max_length=1000, null=False, blank=False)
    inputdate = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name
