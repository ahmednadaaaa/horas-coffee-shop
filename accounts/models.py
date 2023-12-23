from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    image = models.ImageField(_("Image"), upload_to='Profile_img', blank=True, null=True)
    join_date = models.DateTimeField(_("join date"), default=datetime.datetime.now)
    product_favorits = models.ManyToManyField(Product)  # تم تصحيح اسم الحقل هنا

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return '%s' % (self.user)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
