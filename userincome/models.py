from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Source(models.Model):  # Keep this above UserIncome for clarity
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserIncome(models.Model):
    amount = models.FloatField()  # Consider using DecimalField in future
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.ForeignKey(to=Source, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.source.name} - {self.amount}"

    class Meta:
        ordering = ['-date']
