# Generated by Django 3.1.2 on 2020-11-13 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account_users', '0005_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='cartitems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cost', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('dis_price', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(choices=[('S', 'Shirt'), ('SW', 'Sport Wear'), ('OW', 'Out Wear')], max_length=2)),
                ('description', models.CharField(blank=True, default=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='orderitems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentmethod', models.CharField(choices=[('COD', 'Cash On Delivery'), ('UPI', 'UPI'), ('DC', 'Debit Card'), ('CC', 'Credit Card')], max_length=3)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=False)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account_users.useraddress')),
                ('items', models.ManyToManyField(to='core.cartitems')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cartitems',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.items'),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
