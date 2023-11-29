
from django.urls import path
from . import views

# assigning app name to include in urls
app_name="home"

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("detail/<int:post_id>",views.HomeDetail.as_view(),name="detail")
]