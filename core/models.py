from django.db import models
from django.conf import settings
from account_users.models import UserAddress



CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sport Wear'),
    ('OW','Out Wear')
)
PAYMENT_CHOICES = (
    ('COD','Cash On Delivery'),
    ('UPI','UPI'),
    ('DC','Debit Card'),
    ('CC','Credit Card')
)

# Create your models here.


class items(models.Model):
    title = models.CharField(max_length=300)
    price = models.FloatField()
    dis_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    description =models.CharField(blank=True,default=True,max_length=1000)
    
    def __str__(self):
        return self.title
    


class cartitems(models.Model):
    item = models.ForeignKey(items, on_delete=models.CASCADE)
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cost = models.FloatField(blank=True,null=True)


    def __str__(self):
        return  f"{self.user.username} -  {self.item.title} - {self.quantity}"
    


class Promo(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    name = models.CharField(max_length=20)
    min_amount = models.CharField(max_length=5)
    discount = models.CharField( max_length=10)
    quantity = models.CharField(blank=True,max_length=3)

    def __str__(self):
        return self.name



class orderitems(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(cartitems,blank=True)
    payment = models.CharField(choices=PAYMENT_CHOICES,max_length=3)
    promo = models.ForeignKey(Promo,on_delete=models.SET_NULL,null=True,blank=True)
    total = models.CharField(max_length=20,default=False)
    ordered_date = models.DateTimeField(auto_now_add=True,blank=True)
    address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL,null=True,blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + "-"+str(self.ordered_date)
    