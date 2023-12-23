from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Product, through='OrderDetail')   # through جيب ال منج من خلال order details
    is_finished = models.BooleanField()
    total = 0
    items_count = 0

    def __str__(self):
        return 'User: ' + self.user.username + 'Order id' + str(self.id)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return 'User: ' + self.order.username + ', Product: ' +self.product.name + ', Order id: ' + str(self.order.id)

    class Meta:
        ordering=['id'] # هيرتب العرض من القديم للاحدث



