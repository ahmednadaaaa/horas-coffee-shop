from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("price"))
    photo = models.ImageField(upload_to="img", default="", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name