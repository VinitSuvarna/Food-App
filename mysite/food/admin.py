from django.contrib import admin
from food.models import FoodItemsModel, LogHistoryModel, Order

# Register your models here.
# -------------------------------------------------------------------------------------------- 
admin.site.register(FoodItemsModel)
admin.site.register(LogHistoryModel)
from food.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'item__item_name')
