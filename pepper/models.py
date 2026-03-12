from django.db import models
from django.contrib.auth.models import User

class Data(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    amount = models.IntegerField()


class Cart(models.Model):
    product = models.ForeignKey(Data,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):

    order_id = models.CharField(max_length=100, unique=True, default="TEMP")

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    address = models.TextField()
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)

    payment_method = models.CharField(max_length=50, default="COD")

    total_amount = models.IntegerField()

    status = models.CharField(max_length=100, default="Order Placed")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    pincode = models.CharField(max_length=10)

    district = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username