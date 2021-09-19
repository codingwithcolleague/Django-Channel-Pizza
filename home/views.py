import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    pizza = Pizza.objects.all()
    order = Order.objects.filter( user = request.user)
    context = { "pizza" : pizza , "orders" : order }
    print("contextttt",context)
    return render(request,"index.html" ,context)


def orderview(request,order_id):
    order = Order.objects.filter(order_id =order_id).first()
    if order is  None:
        return redirect("/")
    context = {"order"  : order }
    return render(request,"order.html",context)

@csrf_exempt
def order_pizza(request):
    user = request.user
    data = json.loads(request.body)
    try:
        pizza = Pizza.objects.get(id=data.get('id'))
        order = Order(user=user, pizza=pizza,amount=pizza.price )
        order.save()
        return JsonResponse({ "message" : "success" })
    except Pizza.DoesNotExist:
        return JsonResponse({ "error" : "something went worng" })