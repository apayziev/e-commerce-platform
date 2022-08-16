from django.db import models
from helpers.models import BaseModel

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    in_stock = models.PositiveIntegerField()

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name
