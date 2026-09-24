from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("products.urls")
    ),

    path(
        "i18n/",
        include("django.conf.urls.i18n")
    ),
] 

urlpatterns += i18n_patterns(
    path("", include("products.urls")),
)

#Media files (product images)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
