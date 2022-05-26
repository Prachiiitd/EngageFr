from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Application(models.Model):
    appId = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    images = models.ImageField(upload_to='images/', blank=True, null=True)
    found = models.BooleanField(default=False)
    lastTrackDate = models.DateTimeField(null=True)
    lastTrackLoc = models.CharField(max_length=100, default='NA')

    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Application"

    def __str__(self):
        return self.fName

    def delete(self, using=None, keep_parents=False):
        self.images.storage.delete(self.images.name)
        super().delete()

