from django.db import models

# Create your models here.
class Category(models.Model):
    slug=models.SlugField(("Slug"))
    title=models.CharField(("Title"), max_length=255)

    def __str__(self) -> str:
        return self.title
    
class MenuItem(models.Model):
    title=models.CharField(("Title"), max_length=255)
    price=models.DecimalField(("Price"), max_digits=6, decimal_places=2)
    inventory=models.SmallIntegerField(("Inventory"))
    category=models.ForeignKey(Category, on_delete=models.PROTECT,default=1)