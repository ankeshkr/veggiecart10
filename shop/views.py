from django.shortcuts import render

from .models import Product,Contact,Order,OrderUpdate
from math import ceil
from django.http import HttpResponse
import json

# Create your views here.
def searchMatch(query,item):
    #print("prodtemp")
    if query in item.desc or query in item.product_name or query in item.category:
        return True
    else:
        return False
  #  '''return True only if query matched the item'''
   # if query in item.desc or query in item.product_name or query in item.category: 
    # return True
    #else

def search(request):
    query=request.GET.get('search')
    allProds=[]
    catprods = Product.objects.values('category', 'id')
   # print(catprods)
    cats= {item['category'] for item in catprods}
   # print(cats)
    for cat in cats:
        print("inside for")
        prodtemp=Product.objects.filter(category=cat)
        
        prod = [item for item in prodtemp if searchMatch(query,item)]
        #prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4 + ceil(n/4 -(n//4))
        if len(prod)!=0:
            allProds.append([prod,range(1,nSlides), nSlides])
    params={'allProds':allProds}
    #print(params)

    return render(request,"shop/index.html",params)
  ##  return render(request,"shop/search.html")
def index(request):
   ## products=Product.objects.all()
    #print(products)
    #n=len(products)
    #nSlides=n//4 + ceil(n/4 -(n//4))
    allProds=[]
    catprods = Product.objects.values('category', 'id')
   # print(catprods)
    cats= {item['category'] for item in catprods}
    # print(cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        #print(prod)
        n=len(prod)
        nSlides=n//4 + ceil(n/4 -(n//4))
        allProds.append([prod,range(1,nSlides), nSlides])
    #params={'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    #allProds = [[products, range(1,nSlides), nSlides],
     #           [products, range(1,nSlides), nSlides]]
    params={'allProds':allProds}
  #  print(params)

    return render(request,"shop/index.html",params)

def about(request):
    return render(request,"shop/about.html")

def contact(request):
    if request.method =='POST':
        print(request)
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        print(name,email,phone,desc)
        contact=Contact(name=name, email=email,phone=phone,desc=desc)
        contact.save()
    return render(request,"shop/contact.html")

def tracker(request):
    if request.method =='POST':
      #  print(request)
        OrderId=request.POST.get('OrderId','')
        email=request.POST.get('email','')
        #return HttpResponse(f"{OrderId} and {email}")
        try:
            order=Order.objects.filter(order_id=OrderId, email=email)
            #return HttpResponse(f"{order} and {email}")
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=OrderId)
                updates=[]
                for item in update:
                    #return HttpResponse(f"{order} and {email}")
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse("{}")
    return render(request,"shop/tracker.html")


def ProdView(request, myid):
    # fetch the product using ID
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request,"shop/prodview.html",{'product':product[0]})

def Checkout(request):
    if request.method =='POST':
        print(request)
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        thank=True
        order=Order(items_json=items_json, name=name, email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        #id=order.order_id
        order.save()
        update=OrderUpdate(order_id=order.order_id, update_desc="the order has been placed")
        update.save()
        id=order.order_id
        return render(request,"shop/checkout.html",{'thank':thank,'id':id})
    return render(request, 'shop/checkout.html')