"""
URL configuration for NFTgallery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from oauth2_provider.views import TokenView, RevokeTokenView
#
from orders.views import BuyProductView
#

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # my apps
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),

    # def-spectacular
    path('gtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('gtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('gtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # oAuth2
    path('createtoken/', TokenView.as_view(), name='create_token'),
    path('revoketoken/', RevokeTokenView.as_view(), name='revoke_token'),
    path('go-to-getway/<int:user_id>/<int:price>/', BuyProductView.as_view())
]
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# admin panel
admin.site.site_title = "GalleryAP"
admin.site.index_title = "Control Panel"
admin.site.site_header = "WELCOME Boss"
