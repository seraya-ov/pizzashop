from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from shopapp.forms import UserForm, UserFormForEdit, ProductForm
from shopapp.models import Product

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.

def home(request):
	return redirect(shop_home)

@login_required(login_url='/shopapp/sign_in/')
def shop_account(request):
	user_form = UserFormForEdit(instance=request.user)

	if request.method == "POST":
		user_form = UserFormForEdit(request.POST, instance=request.user)

		if user_form.is_valid():
			user_form.save()

	return render(request, 'shopapp/account.html', {
		'user_form': user_form,
	})

@login_required(login_url='/shopapp/sign_in/')
def shop_shop(request):
    products = Product.objects.order_by("-id")
    if request.user.is_superuser == True:
        return render(request, 'shopapp/shop.html', {'products': products})
    else:
        return render(request, 'shopapp/shop_for_users.html', {'products': products})

@login_required(login_url='/shopapp/sign_in/')
def shop_chosen_items(request):
	products = Product.objects.filter(owners=request.user).order_by("-id")
	return render(request, 'shopapp/chosen_items.html', {
		'products': products
	})

@login_required(login_url='/shop/sign_in/')
def shop_add_product(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect(shop_shop)

    return render(request, 'shopapp/add_product.html', {
        'form': form
    })

@login_required(login_url='/shop/sign_in/')
def shop_edit_product(request, product_id):
    form = ProductForm(instance = Product.objects.get(id = product_id))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance = Product.objects.get(id = product_id))
        if form.is_valid():
            product = form.save()
            return redirect(shop_shop)

    return render(request, 'shopapp/edit_product.html', {
        'form': form
    })


@login_required(login_url='/shop/sign_in/')
def shop_pick_product(request, product_id):
    product = Product.objects.get(id = product_id)
    return render(request, 'shopapp/pick.html', {
        'product': product,
        'page': request.path
    })

@login_required(login_url='/shop/sign_in/')
def shop_choose_product(request, product_id):
    product = Product.objects.get(id = product_id)
    product.owners.add(request.user)
    product.save()
    if request.user.is_superuser == True:
        return render(request, 'shopapp/shop.html', {'products': Product.objects.order_by("-id")})
    else:
        return render(request, 'shopapp/shop_for_users.html', {'products': Product.objects.order_by("-id")})

@login_required(login_url='/shop/sign_in/')
def shop_return_product(request, product_id):
    product = Product.objects.get(id = product_id)
    product.owners.clear()
    product.save()
    return render(request, 'shopapp/chosen_items.html', {
        'products': Product.objects.filter(owners=request.user).order_by("-id")
    })

@login_required(login_url='/shop/sign_in/')
def shop_delete_product(request, product_id):
	Product.objects.filter(id = product_id).delete()
	return redirect(shop_shop)


@login_required(login_url='/shopapp/sign_in/')
def shop_home(request):
    return redirect(shop_shop)

def shop_sign_up(request):
	user_form = UserForm()
	if request.method == "POST":
		user_form = UserForm(request.POST)

		if user_form.is_valid():
			new_user = User.objects.create_user(**user_form.cleaned_data)

			login(request, authenticate(
				username = user_form.cleaned_data['username'],
				password = user_form.cleaned_data['password']
			))

			return redirect(shop_home)

	return render(request, 'shopapp/sign_up.html', {
        'user_form': user_form,
    })