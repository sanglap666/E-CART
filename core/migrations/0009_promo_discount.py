# Generated by Django 3.1.2 on 2020-11-15 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20201115_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='discount',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
