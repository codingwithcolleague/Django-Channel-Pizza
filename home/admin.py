from django.contrib import admin
from .models import Order,Pizza
# Register your models here.
from home.models import Order,Pizza

admin.site.register(Pizza)
admin.site.register(Order)
