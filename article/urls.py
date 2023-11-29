from . import views
from django.urls import path

# assigning app_name to include in urls
app_name = "article"

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('article_plus/', views.article_plus, name='article_plus'),
]
