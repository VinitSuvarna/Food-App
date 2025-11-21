from django.contrib import admin
from food.models import FoodItemsModel, LogHistoryModel

# Register your models here.
# -------------------------------------------------------------------------------------------- 
admin.site.register(FoodItemsModel)
admin.site.register(LogHistoryModel)
