# Generated by Django 4.1.7 on 2023-06-10 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finding_china', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default='https://cdn-icons-png.flaticon.com/512/105/105544.png', max_length=500, upload_to='profile_pictures/'),
        ),
    ]
