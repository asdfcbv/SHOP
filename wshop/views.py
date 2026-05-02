from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Q


def index(request):
    categories = Category.objects.all()
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'index.html', {
        'categories': categories,
        'products': products,
        'query': query
    })


def products_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'products.html', {
        'category': category,
        'products': products,
        'categories': categories
    })


def product_detail(request, product_id):
    """
    Страница одного товара
    """
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {
        'product': product
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('product_detail', product_id=product_id)


def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        price = product.get_price()
        total += price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': price * quantity
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart

    return redirect('cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')