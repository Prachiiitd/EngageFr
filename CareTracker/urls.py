"""CareTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Url for admin page

    # Url included fom Customer App with starting path as /customer
    path('customer/', include(('Customer.urls', 'Customer'), namespace="Customer")),

    # Url included fom Auth App with starting path as /auth
    path('auth/', include(('Auth.urls', 'Auth'), namespace="Auth")),

    path('', views.index, name="index")  # Url for the index page in the Car tracker app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
