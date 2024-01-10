from django.shortcuts import render
from shop.models import product
from django.db.models import Q
# Create your views here.
def searchresult(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        products=product.objects.all().filter(Q(name__icontains=query) | Q(description__icontains=query))
        print(products)
        return render(request,'search.html',{'query':query,'products':products})