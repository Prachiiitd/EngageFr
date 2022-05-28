from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    """
    Customer Model
    .user: User
    .fName: First Name
    .lName: Last Name
    .email: Email
    """
    # One-to-one relationship with Django User model (one user can have only one customer which is unique)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user')
    email = models.CharField(max_length=100, null=False)
    fName = models.CharField(max_length=100, null=False)
    lName = models.CharField(max_length=100, null=False)

    class Meta:
        """
        Metaclass for Customer model
        .db_table: name of the table in the database
        """

        db_table = "Customer"

    def __str__(self):
        return self.fName  # object representation in string format (for admin)


class CameraIP(models.Model):
    """
    CameraIP Model
    .ipaddress: IP Address
    .address: Address
    """
    ipaddress = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "CameraIP"  # name of the table in the database

    def __str__(self):
        return self.ipaddress  # object representation in string format (for admin)
