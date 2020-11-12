from django.shortcuts import render,redirect
from .models import items,cartitems
from django.views.generic import ListView,DetailView
from .forms import AddressForm

# Create your views here.
def homeview(request):
    if request.user.is_authenticated:
        return render(request,'home.html',{'total':cart_quantity(request)})        
    else:
        return render(request,'home.html')


def productview(request):
    object_list = items.objects.all()
    if request.user.is_authenticated:
        
        return render(request,'products.html',{'total':cart_quantity(request),'object_list':object_list})
    else:
        
        return render(request,'products.html',{'object_list':object_list})    


def productdetailview(request,pk):
    if request.user.is_authenticated:
        
        item = items.objects.get(pk=pk)
        return render(request,'product.html',{'object':item,'total':cart_quantity(request)})
    else:
        
        item = items.objects.get(pk=pk)
        return render(request,'product.html',{'object':item,})   


def add_cart(request,pk):

   
    if request.user.is_authenticated:
    
        item = items.objects.get(pk=pk)
        cart_item,boolval = cartitems.objects.get_or_create(user=request.user,item=item)         #if boolval = false then item is already present
        
        if not boolval:
            
            cart_item.quantity = cart_item.quantity + 1
            cart_item_cost(request,cart_item)
            
        else:
            if cart_item.item.dis_price:
                cart_item.cost = cart_item.item.dis_price 
            else:
                cart_item.cost = cart_item.item.price 
            cart_item.save()   
        
        return redirect('products') 
    else:
        
        return productdetailview(request,pk)

def cart(request):
    
    if request.method == 'GET':
        cart_items = cartitems.objects.filter(user=request.user)
        cost,dis  = total_cost(request)
        return render(request,'cart.html',{'total':cart_quantity(request),'cart':cart_items,'cost':cost,'discount':dis})

    elif request.method == 'POST':
        print(request.POST.items)
        cart_item = cartitems.objects.get(pk=request.POST.get('pk'))
        if (request.POST.get('update')):
        
            cart_item.quantity = int(request.POST.get('quantity'))
            cart_item.save()
            cart_item_cost(request,cart_item)
        elif (request.POST.get('remove')):
            cart_item.delete()
        
        return redirect('cart')

def checkout(request):
    form1 = AddressForm(request.POST or None)

    cart_items = cartitems.objects.filter(user=request.user)
    cost,dis  = total_cost(request)
    context= {
        'total':cart_quantity(request),
        'cartitems':cart_items,
        'cost':cost,
        'form1':form1        


    }



    return render(request,'checkout.html',context)
def cart_quantity(request):
    total_quantity = 0
    cart_items = cartitems.objects.filter(user=request.user)
    if cart_items.exists():
        for item in cart_items:
            total_quantity = total_quantity + item.quantity
    return total_quantity        

def cart_item_cost(request,cart_item):
    if cart_item.item.dis_price:
            cart_item.cost = cart_item.item.dis_price * cart_item.quantity
    else:
            cart_item.cost = cart_item.item.price * cart_item.quantity
    cart_item.save()

def total_cost(request):    
    cart_items = cartitems.objects.filter(user=request.user)
    cost = 0
    cost1 = 0
    for item in cart_items:
        if item.item.dis_price: 
            cost = cost + item.item.dis_price 
        else:
            cost = cost + item.item.price   
        cost1 = cost1 + item.item.price 
    discount = cost1 - cost    
    return cost,discount        