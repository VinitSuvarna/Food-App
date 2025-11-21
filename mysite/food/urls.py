from django.urls import path
from food import views

app_name = 'food'

urlpatterns = [
   
    # http://localhost:8000/food/home/
    # function based home view
    # ---------------------------------------------------------------------------------------------
     path('home/', views.HomeFunctionView, name='home'),
   
   
   
    # http://localhost:8000/food/home/
    # class based home view
    # ---------------------------------------------------------------------------------------------
    #path('home/', views.HomeClassView.as_view(), name='home'),
   
   
   
    # http://localhost:8000/food/detail/1/
    # function based detail view
    # ---------------------------------------------------------------------------------------------
     path('detail/<int:item_id>/', views.DetailFunctionView, name='detail'),
   
   
   
    # http://localhost:8000/food/detail/1/
    # class based detail view
    # ---------------------------------------------------------------------------------------------
    # path('detail/<int:pk>/', views.DetailClassView.as_view(), name='detail'),
   
   
   
    # http://localhost:8000/food/add/
    # function based create item view
    # ---------------------------------------------------------------------------------------------
    # path('add/', views.CreateFoodItemFunctionView, name='add'),
   
   
   
    # http://localhost:8000/food/add/
    # class based create item view
    # ---------------------------------------------------------------------------------------------
    path('add/', views.CreateFoodItemClassView.as_view(), name='add'),
   
   
   
    # http://localhost:8000/food/update/
    # ---------------------------------------------------------------------------------------------
    path('update/<int:item_id>/', views.UpdateFoodItemFunctionView, name='update'),
   
   
   
    # http://localhost:8000/food/delete/
    # ---------------------------------------------------------------------------------------------
    path('delete/<int:item_id>/', views.DeleteFoodItemFunctionView, name='delete'),
   
]