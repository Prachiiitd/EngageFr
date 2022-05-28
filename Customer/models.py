from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Application(models.Model):
    """
    Application Model
    .appId: Application ID
    .fName: First Name
    .lName: Last Name
    .images: Image
    .found:  Field to check if the application is found or not.
    .lastTrackDate: # Last track date is the date and time when the application was last tracked.
    .lastTrackLoc: # Last track Camera ID by which the application was last tracked.
    .customer: # Customer who owns the application.
    (found, lastTrackDate, lastTrackLoc are updated by the background process which will running continuously using
    a different pythin script)
    """

    appId = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    images = models.ImageField(upload_to='images/', blank=True, null=True)
    found = models.BooleanField(default=False)
    lastTrackDate = models.DateTimeField(null=True)
    lastTrackLoc = models.CharField(max_length=100, default='NA')

    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """
        Metaclass for Application model
        """
        db_table = "Application"  # name of the table in the database

    def __str__(self):
        """
        Object representation in string format (for admin)
        """
        return self.fName

    def delete(self, using=None, keep_parents=False):
        """
        Overriding the delete method to delete the image from the server.
        """
        self.images.storage.delete(self.images.name)  # delete the image from the server
        super().delete()  # delete the application from the database

