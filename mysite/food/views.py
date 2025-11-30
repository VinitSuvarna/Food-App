from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from food.models import FoodItemsModel, LogHistoryModel, Order
from food.forms import FoodItemsForm


# Create your views here.
# --------------------------------------------------------------------------------------------- 


# function based home view 
# --------------------------------------------------------------------------------------------- 
# function based home view
# ---------------------------------------------------------------------------------------------
def HomeFunctionView(request):
    if request.user.is_authenticated and request.user.profilemodel.user_type == 'ADMIN':
        item_list = FoodItemsModel.objects.all()
   
    elif request.user.is_authenticated and request.user.profilemodel.user_type == 'CUSTOMER':
        item_list = FoodItemsModel.objects.all()
   
    elif request.user.is_authenticated and request.user.profilemodel.user_type == 'RESTAURANT':
        item_list = FoodItemsModel.objects.filter(restaurant_owner=request.user.id)
   
    else:
        item_list = FoodItemsModel.objects.all()
   
    context = {
        "item_list": item_list
    }
   
    return render(request, "food/home.html", context)
# Class based delete item view
# ---------------------------------------------------------------------------------------------
class HomeClassView(ListView):
    model = FoodItemsModel
    template_name = "food/home.html"
    context_object_name = "item_list"

    def get_queryset(self):
        return FoodItemsModel.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_list'] = self.get_queryset()
        return context

# function based detail view 
# --------------------------------------------------------------------------------------------- 
def DetailFunctionView(request, item_id):
    item = FoodItemsModel.objects.get(id=item_id)

    object_lh = LogHistoryModel.objects.all()
    

    context = {
        'item': item
        ,'object_lh': object_lh,
    }
    
    return render(request, "food/detail.html", context)

# Class based detail view
# ---------------------------------------------------------------------------------------------
class DetailClassView(DetailView):
    model = FoodItemsModel
    template_name = "food/detail.html"
    context_object_name = "item"

    def get_object(self, queryset=None):
        return FoodItemsModel.objects.get(id=self.kwargs['pk'])
    
# Class based create item view
# --------------------------------------------------------------------------------------------- 
class CreateFoodItemClassView(CreateView):
    model = FoodItemsModel
    fields = ['prod_code','restaurant_owner', 'item_name', 'item_description', 'item_price', 'item_image']
    template_name = "food/food-items-form.html"
    success_url = reverse_lazy('food:home')

    def form_valid(self, form):
        form.instance.admin = self.request.user.username

        # logging the record to the history table
        object_log_history = LogHistoryModel(
            log_username=self.request.user.username,
            log_prod_code=form.instance.prod_code,#self.request.POST.get("prod_code")
            log_item_name=form.instance.item_name,#self.request.POST.get("item_name")
            log_operation_type="CREATE"
        )
        object_log_history.save()
        return super().form_valid(form)


# function based create item view 
# --------------------------------------------------------------------------------------------- 
def CreateFoodItemFunctionView(request):
    form = FoodItemsForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("food:home")

        
    


    context = {
        "form": form

    }

    return render(request, "food/food-items-form.html", context)


# function based update item view
# ---------------------------------------------------------------------------------------------
def UpdateFoodItemFunctionView(request, item_id):
    item = FoodItemsModel.objects.get(id=item_id)
    form = FoodItemsForm(request.POST or None, instance=item)
   
    context = {
        'form': form
    }
   
    if form.is_valid():
        form.save()

        # logging the record to the history table
        object_log_history = LogHistoryModel(
            log_username=request.user.username,
            log_prod_code=form.instance.prod_code,#self.request.POST.get("prod_code")
            log_item_name=form.instance.item_name,#self.request.POST.get("item_name")
            log_operation_type="Updated"
        )
        object_log_history.save()


        return redirect('food:detail', item_id=item_id)
   
    return render(request, "food/food-items-form.html", context)


# function based delete item view
# ---------------------------------------------------------------------------------------------

def DeleteFoodItemFunctionView(request, item_id):
    item = FoodItemsModel.objects.get(id=item_id)

    context = {
        'item': item

    }

    if request.method == 'POST':

        # logging the record to the history table

        object_log_history = LogHistoryModel(
            log_username=request.user.username,
            log_prod_code=item.prod_code,
            log_item_name=item.item_name,
            log_operation_type="Deleted"
        )

        object_log_history.save()

        item.delete()
        return redirect('food:home')

    return render(request, "food/item-delete.html", context)

 # place order view
# ---------------------------------------------------------------------------------------------
@login_required
def PlaceOrderFunctionView(request, item_id):
    item = get_object_or_404(FoodItemsModel, id=item_id)

    if request.method == "POST":
        # get quantity from form
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1
        if quantity < 1:
            quantity = 1

        # create order with PENDING status
        order = Order.objects.create(
            customer=request.user,
            item=item,
            quantity=quantity,
            price_at_order=item.item_price,
            status='PENDING',
        )

        # later we'll send this to PayPal
        return redirect('food:order_detail', order_id=order.id)

    # GET request: simple confirm page
    context = {
        'item': item
    }
    return render(request, "food/order_confirm.html", context)


# order detail view
# ---------------------------------------------------------------------------------------------
@login_required
def OrderDetailFunctionView(request, order_id):
    user = request.user

    # Admins / superusers can view any order
    if user.is_superuser or getattr(user, 'profilemodel', None) and getattr(user.profilemodel, 'user_type', '') == 'ADMIN':
        order = get_object_or_404(Order, id=order_id)
    else:
        # Normal customers can view only their own orders
        order = get_object_or_404(Order, id=order_id, customer=user)

    # mark as paid if ?paid=1
    if request.GET.get('paid') == '1' and order.status != 'PAID':
        order.status = 'PAID'
        order.save()

    context = {
        'order': order,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        'paypal_currency': settings.PAYPAL_CURRENCY,
    }
    return render(request, "food/order_detail.html", context)
