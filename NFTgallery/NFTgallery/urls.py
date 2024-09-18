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
from azbankgateways.urls import az_bank_gateways_urls
#
from orders.views import BuyProductView
#

urlpatterns = [
    # admin
    path('api/admin/', admin.site.urls),

    # my apps
    path('api/', include('home.urls', namespace='home')),
    path('api/products/', include('products.urls', namespace='products')),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/orders/', include('orders.urls', namespace='orders')),

    # def-spectacular
    path('api/gtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/gtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/gtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # oAuth2
    path('api/ogtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # bank-gateways
    path('bank/', az_bank_gateways_urls()),
    path('go-to-getway/<int:user_id>/<int:price>/', BuyProductView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# admin panel
admin.site.site_title = "GalleryAP"
admin.site.index_title = "Control Panel"
admin.site.site_header = "WELCOME Boss"
