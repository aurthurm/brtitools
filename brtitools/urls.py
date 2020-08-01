from django.contrib import admin
from django.urls import path, re_path, include
from .views import IndexView
from django.conf import settings
from django.conf.urls.static import serve
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serve Vue Application
IndexView = never_cache(TemplateView.as_view(template_name='index.html'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView, name="index"),
    path('api/', include('api.urls', namespace="brtitools-api")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^_nuxt/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
