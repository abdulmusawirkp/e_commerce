from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    #price = models.PositiveBigIntegerField()
    # stock = models.PositiveIntegerField(null=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ProductVarient(models.Model):
    varientname = models.CharField(max_length=100,null=True)
    varstock = models.PositiveIntegerField(null=True)
    # varprice = models.PositiveIntegerField(null=True)
    varprice = models.PositiveBigIntegerField()
    proname = models.ForeignKey(Product, related_name='variants',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proname} / {self.varientname}"
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    images = models.ImageField(upload_to='media',null=True)


    def __str__(self):
        return self.product.name    


class Banner(models.Model):
    title=models.CharField(max_length=200)
    discription=models.TextField(max_length=200)
    image=models.FileField(upload_to='banner')

    def __str__(self):
        return self.title
    