from django import views
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

# from .tasks import order_created
from django.urls import reverse

# Create your views here.
class OrderCreate(views.View):
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()

        return render(
            request, "orders/order/order_create.html", {"cart": cart, "form": form}
        )

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # set the order in the session
            request.session["order_id"] = order.id
            # redirect for payment
            return redirect(reverse("payment:process"))

        return render(
            request, "orders/order/order_create.html", {"cart": cart, "form": form}
        )
