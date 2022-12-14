# import braintree
# from django.shortcuts import render, redirect, get_object_or_404
# from django.conf import settings
# from orders.models import Order
from django.views import View

# # instantiate Braintree payment gateway
# gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

# # Create your views here.
# class PaymentProcess(View):
#     def get(self, request):
#         order_id = request.session.get("order_id")
#         order = get_object_or_404(Order, id=order_id)
#         client_token = braintree.ClientToken.generate()
#         return render(
#             request,
#             "payment/payment_process.html",
#             {"order": order, "client_token": client_token},
#         )

#     def post(self, request):
#         nonce = request.POST.get("payment_method_nonce", None)
#         order_id = request.session.get("order_id")
#         order = get_object_or_404(Order, id=order_id)
#         result = braintree.Transaction.sale(
#             {"amount": f"{order.get_total_cost():.2f}", "payment_method_nonce": nonce}
#         )
#         if result.is_success:
#             order.paid = True
#             order.braintree_id = result.transaction.id
#             order.save()
#             return redirect("payment:done")
#         else:
#             return redirect("payment:canceled")

import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == "POST":
        # retrieve nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction
        result = gateway.transaction.sale(
            {
                "amount": f"{total_cost:.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect("payment:done")
        else:
            return redirect("payment:canceled")
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            "payment/payment_process.html",
            {"order": order, "client_token": client_token},
        )


class PaymentDone(View):
    def get(self, request):
        return render(request, "payment/payment_done.html")


class PaymentCanceled(View):
    def get(self, request):
        return render(request, "payment/payment_canceled.html")
