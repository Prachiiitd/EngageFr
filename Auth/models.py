from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user')
    email = models.CharField(max_length=100, null=False)
    fName = models.CharField(max_length=100, null=False)
    lName = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "Customer"

    def __str__(self):
        return self.fName

