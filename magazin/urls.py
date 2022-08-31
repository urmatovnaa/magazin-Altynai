from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core.views import ProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', ProductView.as_view({'get': 'list', 'post': 'create'})),
    path('product/<int:pk>', ProductView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
