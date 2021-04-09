from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True)),  # перенаправим корневой URL нашего сайта 127.0.0.1:8000 на 127.0.0.1:8000/catalog/
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
