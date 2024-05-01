from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q
import json
from .forms import UserRegisterForm, UserLoginForm
from .models import *


def index(request):
    template_name = "web/header.html"
    return render(request, template_name)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email']
            )
            messages.success(request, 'Register complete')
            return redirect('login')
        else:
            messages.error(request, 'Register not complete')
    else:
        form = UserRegisterForm()
    return render(request, 'web/register.html', {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'web/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect('index')

def cab(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        context = {'customer': customer}
        return render(request, 'web/cab.html', context)
    else:
        return redirect('login')

def my_orders(request):
    if request.user.is_authenticated:
        return render(request, "web/cab/my-orders.html")
    else:
        return redirect('login')

def my_shopping_cart(request):
    if request.user.is_authenticated:
        return render(request, "web/cab/my-shopping-cart.html")
    else:
        return redirect('login')

def my_wallet(request):
    if request.user.is_authenticated:
        return render(request, "web/cab/my-wallet.html")
    else:
        return redirect('login')

def add_product(request):
    if request.user.is_authenticated:
        products = {'products': Product.objects.all()}
        categories = Category.objects.all()
        return render(request, "web/add_product.html", {'categories': categories})
    else:
        return redirect('login')

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Фільтрація за категоріями
    selected_categories = request.GET.getlist('categories')
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # Фільтрація за роком випуску
    year = request.GET.get('year')
    if year:
        products = products.filter(Q(year_from__lte=year) & Q(year_to__gte=year))

    # Сортування
    sort_by = request.GET.get('sort_by')
    if sort_by in ['name', 'price', 'manufacturer', 'model_car__name']:
        products = products.order_by(sort_by)

    manufacturers = Product.objects.values_list('manufacturer', flat=True).distinct()
    model_cars = Product.objects.values_list('model_car__name', flat=True).distinct()
    context = {'products': products, 'categories': categories, 'manufacturers': manufacturers, 'modelCars': model_cars}
    return render(request, "web/shop.html", context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = product.category.all()
    context = {'product': product, 'categories': categories}
    return render(request, "web/detail.html", context)

def upadateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def cart(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        categories = Category.objects.all()
        customer, created = Customer.objects.get_or_create(user=request.user, defaults={'name': request.user.username, 'email': request.user.email})
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False, 'products': products, 'categories': categories}
    return render(request, 'web/cart.html', context)

def checkout(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False, 'categories': categories}
    return render(request, 'web/checkout.html', context)

def successfully(request):
    try:
        order = Order.objects.filter(customer=request.user.customer, complete=False).latest('date_ordered')
        order.mark_as_complete()  # Mark the latest incomplete order as complete
    except Order.DoesNotExist:
        pass
    
    context = {'order': order}
    template_name = "web/complete.html"
    return render(request, template_name, context)
