from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    Price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image_URL(self):
        try:
            url = self.image.url
        except:
            url = "{% static 'images/placeholder.png' %}"
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=False, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_order_price(self):
        items = self.get_all_order_items
        total_order_price = 0
        for item in items:
            total_order_price = total_order_price+item.calculate_total
        return total_order_price

    @property
    def total_quantity(self):
        items = self.get_all_order_items
        print(items)
        total_items = 0
        if len(items) > 0:
            for item in items:
                total_items = total_items+item.quantity
        return total_items

    @property
    def get_all_order_items(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_total(self):
        total = self.product.Price*self.quantity
        return total

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
