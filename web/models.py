# models.py

import datetime
from django.db import models
from django.contrib.auth.models import User
import uuid


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_reg = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name



class Manufacturer(models.Model):
    name= models.CharField(max_length=100, db_index=True)
    def __str__(self):
      return f"{self.name}" 


class Model_car(models.Model):
    name= models.CharField(max_length=100, db_index=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    def __str__(self):
      return f" {self.manufacturer.name} {self.name} "
    
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)     
    model_car = models.ForeignKey(Model_car, on_delete=models.CASCADE, verbose_name='Model Car')       
    year_from = models.IntegerField(default=datetime.datetime.now().year)
    year_to = models.IntegerField(default=datetime.datetime.now().year)    
    category = models.ManyToManyField("Category", related_name='products')
    available = models.BooleanField(default=True)
    
    def __str__(self):
     return f"{self.name} ({self.id})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/')  # Оновлений шлях

    def __str__(self):
        return self.product.name + ' Image'


class Order(models.Model):
        customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
        date_ordered = models.DateTimeField(auto_now_add=True)
        complete = models.BooleanField(default=False, null=True, blank=True)
        transaction_id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

        def __str__(self):
            return str(self.id)

        @property
        def shipping(self):
            shipping = False
            orderitems = self.orderitem_set.all()
            for i in orderitems:
                if i.product.digital == False:
                    shipping = True
            return shipping

        @property
        def get_cart_total(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.get_total for item in orderitems])
            return total

        @property
        def get_cart_items(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.quantity for item in orderitems])
            return total
        
        def mark_as_complete(self):
            self.complete = True
            self.save()


class OrderItem(models.Model):
        product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
        order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
        quantity = models.IntegerField(default=0, null=True, blank=True)
        date_added = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.product.name
        @property
        def get_total(self):
            total = self.product.price * self.quantity
            return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
