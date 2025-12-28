from django.db import models
from django.conf import settings
from farmers.models import Crop, FarmerProfile

User = settings.AUTH_USER_MODEL


# orders/models.py
class Order(models.Model):
    consumer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    farmer = models.ForeignKey(
        FarmerProfile,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("paid", "Paid"),
            ("cancelled", "Cancelled"),
        ],
        default="pending"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_done = models.BooleanField(default=False)

    paid_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

    def calculate_total(self):
        total = sum(
            item.quantity * item.price_per_kg
            for item in self.items.all()
        )
        self.total_amount = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price_per_kg



# class Notification(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='notifications'
#     )
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.username}"
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

