# Generated by Django 4.0.4 on 2022-05-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='lastTrackDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='lastTrackLoc',
            field=models.CharField(default='NA', max_length=100),
        ),
    ]
