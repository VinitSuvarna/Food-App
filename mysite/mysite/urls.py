from django.contrib import admin
from django.urls import path, include
from users import views as UserViews

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView   # 👈 add this

urlpatterns = [
    path("admin/", admin.site.urls),

    # redirect "/" → "/food/home/"
    path("", RedirectView.as_view(url="/food/home/", permanent=False)),

    path("food/", include("food.urls")),
    path("register/", UserViews.RegisterFunctionView, name="register"),
    path("login/", UserViews.LoginFunctionView, name="login"),
    path("logout/", UserViews.LogoutFunctionView, name="logout"),
    path("profile/", UserViews.ProfileFunctionView, name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
