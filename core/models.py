from django.db import models
from django.conf import settings



CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sport Wear'),
    ('OW','Out Wear')
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
    


class orderitems(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(cartitems)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    