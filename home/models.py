import channels
from django.db import models
import random
import string
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync ,sync_to_async
from channels.layers import get_channel_layer
import json
from  django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=300)
    price = models.CharField(max_length=300)
    image = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name
    
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return '' . join(random.choice(chars) for _ in range(size))

CHOICES = (
    ("Order Received" , "Order Received"),
    ("Baking" , "Baking"),
    ("Baked" , "Baked"),
    ("Out of delivery" , "Out of delivery"),
    ('Order recieved' , 'Order recieved')
)

class Order(models.Model):
    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100,blank=True)
    amount = models.IntegerField(default=100)
    status = models.CharField(max_length=100,choices=CHOICES,default="Order Received")
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self,*args,**kwargs):
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(Order,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.order_id
    
    @staticmethod
    def give_order_details(order_id):
        print("order" , order_id)
        instance = Order.objects.filter(order_id=order_id).first()
        data = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status
        
        progress_percentage = 20
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out of delivery':
            progress_percentage = 80
        elif instance.status == 'Order recieved':
            progress_percentage = 100

        channel_layer  = get_channel_layer()    
        data['progress'] = progress_percentage
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,{
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )
        
        
@receiver(post_save,sender=Order)
def order_status_handle(sender,instance,created,**kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        data["order_id"] = instance.id
        data["amount"] = instance.amount
        data["status"] = instance.status
        
        progress_percentage = 0
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out of delivery':
            progress_percentage = 80
        elif instance.status == 'Order recieved':
            progress_percentage = 100
        
        channel_layer  = get_channel_layer()    
        data['progress'] = progress_percentage
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,{
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )
        