from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", include("home.urls", namespace="home")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("articles/", include("article.urls", namespace='article')),
    path('qa/', include("qa.urls", namespace='qa'))
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
