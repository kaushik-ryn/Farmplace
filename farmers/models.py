from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class Crop(models.Model):
    farmer = models.ForeignKey(
        FarmerProfile,
        on_delete=models.CASCADE,
        related_name="crops"   # 👈 VERY IMPORTANT
    )
    name = models.CharField(max_length=100)
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.farmer.user.username}"

