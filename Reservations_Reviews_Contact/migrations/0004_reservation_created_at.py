# Generated by Django 4.2.4 on 2023-11-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations_Reviews_Contact', '0003_rename_catactus_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
