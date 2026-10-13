from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLE_CHOICES = (
        ("buyer", "покупатель"),
        ("seller", "продавец")

    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")
    seller_name = models.CharField(max_length=50, null=True, blank=True)
