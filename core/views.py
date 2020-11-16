from django.shortcuts import render,redirect
from .models import items,cartitems,Promo,orderitems
from account_users.models import UserAddress
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
        cost  = total_cost(request)
        return render(request,'cart.html',{'total':cart_quantity(request),'cart':cart_items,'cost':cost,})

    elif request.method == 'POST':
        
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
    
    if request.method == 'POST':
        
        print(request.POST.items)
        if request.POST.get('add'):
            if form1.is_valid():
                address = UserAddress(
                    user = request.user,
                    street = form1.cleaned_data.get('street'),
                    houseno = form1.cleaned_data.get('houseno'),
                    phoneno = form1.cleaned_data.get('phoneno'),
                    name = form1.cleaned_data.get('name'),
                    pincode = form1.cleaned_data.get('pincode'),  
                
                )
                address.save()
            return redirect('checkout')    
        elif request.POST.get('redeem'):
            promos = Promo.objects.filter(users=request.user)
            promo = Promo.objects.get(pk=request.POST.get('redeem'))
            
            
            cost  = total_cost(request)
            if float(promo.min_amount) > cost:
                return redirect('checkout')
            cart_items = cartitems.objects.filter(user=request.user)
            all_address = UserAddress.objects.filter(user=request.user)
            cost = total_cost(request,promo)
            context= {
                'total':cart_quantity(request),
                'cartitems':cart_items,
                'cost':cost,
                'form1':form1,
                'all_address':all_address,
                'promos':promos,
                'promo':promo
            }



            return render(request,'checkout.html',context)
        else:
            
            try:
                adrs = request.POST.getlist('address')
                address = UserAddress.objects.get(pk=adrs[0])
                
            except:
                return redirect('checkout')

            if not request.POST.get('payment'):
                return redirect('checkout')

            
            if request.POST.get('promo'):
                promo = Promo.objects.get(pk=request.POST.get('promo'))
            else:
                promo =''    
            
            
            payment = request.POST.get('payment')
            cart_items = cartitems.objects.filter(user=request.user)
            order_user = orderitems(
                        user=request.user,
                        payment=payment,
                        address=address,
                        total=request.POST.get('cost'),
                        ordered=True
            )
            if promo:
                order_user.promo = promo
            order_user.save()    
            
            for item in cart_items:
                order_user.items.add(item)
                order_user.save()
                
                #item.delete()   
             
            return render(request,'order.html',{'order':order_user})         
            
                
    
   
    else:    
        promos = Promo.objects.filter(users=request.user)
        
        cart_items = cartitems.objects.filter(user=request.user)
        cost  = total_cost(request)
        all_address = UserAddress.objects.filter(user=request.user)
        context= {
            'total':cart_quantity(request),
            'cartitems':cart_items,
            'cost':cost,
            'form1':form1,
            'all_address':all_address,
            'promos':promos,
            'promo':''
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

def total_cost(request,promo=False):    
    cart_items = cartitems.objects.filter(user=request.user)
    cost = 0
    
    for item in cart_items:
        if item.item.dis_price: 
            cost = cost + item.item.dis_price*item.quantity
              
        else:
            cost = cost + item.item.price*item.quantity   
    if promo:
        
        
        cost = cost - float(promo.discount)         
          
    return cost     