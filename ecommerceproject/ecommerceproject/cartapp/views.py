from django.shortcuts import render,redirect,get_object_or_404
from  shop.models import product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product_detail=product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product_detail,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product_detail,
            quantity=1,
            cart=cart
            
        )
        cart_item.save()
    return redirect('cartapp:cart_detail')
def cartdetail(request,total=0,counter=0,cartitems=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            counter +=cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))
def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    productt=get_object_or_404(product,id=product_id)
    cart_item=CartItem.objects.get(product=productt,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_detail')
def full_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    productt=get_object_or_404(product,id=product_id)
    cart_item=CartItem.objects.get(product=productt,cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_detail')
    
    