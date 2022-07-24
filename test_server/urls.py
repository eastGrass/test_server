"""test_server URL Configuration

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
from django.urls import path, include, re_path
from addressesapp import views as addrView
from addressesapp.api import AddressesList

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^docs/', include('rest_framework_swagger.urls')),
    
    re_path(r'^$', addrView.main, name='addressesmain'),
    re_path(r'^book/', addrView.addressesbook,name='addressesbook'),
    re_path(r'^delete/(?P<name>.*)/', addrView.delete_person, name='delete_person'),
    re_path(r'^book-search/', addrView.get_contacts, name='get_contacts'),
    re_path(r'^addresses-list/', AddressesList.as_view(), name='addresseslist'),
    re_path(r'^notfound/', addrView.notfound,name='notfound'),    
]
