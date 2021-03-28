from django.db import models
from users.models import House
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _


# Create your models here.
class HouseChore(models.Model):
    title = models.CharField(max_length=100, default=_("家事"))
    description = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
