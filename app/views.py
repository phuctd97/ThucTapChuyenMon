from django.core import paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import BRAND_CHOICES, Customer, Cart, Product, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from app import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader



class ProductView(View):
    def get(self, request):
        totalitem = 0
        laptop = Product.objects.filter(category='LT')
        component = Product.objects.filter(category='C')
        accessories = Product.objects.filter(category='ACC')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',
                      {'laptop': laptop, 'component': component, 'accessories': accessories, 'totalitem': totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk,)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 150000
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            totalamount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
    else:
        return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 150000
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 150000
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 150000
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)



@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orderplaced': op})

# Laptop
def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='LT')
    elif data == 'Asus' or data == 'Lenovo' or data == 'Macbook' or data == 'Acer' or data == 'Dell' or data == 'HP' or data == 'MSI' or data == 'LG':
        laptops = Product.objects.filter(category='LT').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='LT').filter(
            discounted_price__lt=20000000)
    elif data == 'above':
        laptops = Product.objects.filter(category='LT').filter(
            discounted_price__gt=20000000)
    paginator = Paginator(laptops, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
        page_obj = paginator.page(1)
    except EmptyPage:
        # Nếu page không có item nào, trả về page cuối cùng
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'app/laptop.html', {'laptops': laptops, 'page_obj':page_obj})


# Accessories
def accessories(request, data=None):
    if data == None:
        accessoriess = Product.objects.filter(category='ACC')
    elif data == 'MZ' or data == 'WW' or data == 'TOM' or data == 'TCN' or data == 'AP' or data == 'LGT' or data == 'Asus' or data == 'SS':
        accessoriess = Product.objects.filter(category='ACC').filter(brand=data)
    elif data == 'below':
        accessoriess = Product.objects.filter(category='ACC').filter(
            discounted_price__lt=2000000)
    elif data == 'above':
        accessoriess = Product.objects.filter(category='ACC').filter(
            discounted_price__gt=2000000)
    paginator = Paginator(accessoriess, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
        page_obj = paginator.page(1)
    except EmptyPage:
        # Nếu page không có item nào, trả về page cuối cùng
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'app/accessories.html', {'accessoriess': accessoriess, 'page_obj':page_obj})


# Component
def component(request, data=None):
    if data == None:
        components = Product.objects.filter(category='C')
    elif data == 'TEA' or data == 'SS' or data == 'PTO' or data == 'GG' or data == 'KST':
        components = Product.objects.filter(category='C').filter(brand=data)
    elif data == 'below':
        components = Product.objects.filter(category='C').filter(
            discounted_price__lt=2000000)
    elif data == 'above':
        components = Product.objects.filter(category='C').filter(
            discounted_price__gt=2000000)
    paginator = Paginator(components, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
        page_obj = paginator.page(1)
    except EmptyPage:
        # Nếu page không có item nào, trả về page cuối cùng
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'app/component.html', {'components': components, 'page_obj':page_obj})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Registed successfully")
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 150000
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})

def delete_info(request):
    custid = request.GET.get('custid')
    customer = Customer.objects.get(pk=custid)
    customer.delete()            
    return redirect('profile')

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

class AddressView(View):
    def get(self, request):
        add = Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            district = form.cleaned_data['district']
            province = form.cleaned_data['province']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           district=district, province=province, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Update Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def delete(seff, request):
        pass

def search(request):
    q= request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'app/search.html', {'data':data})
