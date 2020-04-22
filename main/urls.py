from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = [
    path("",views.home,name="home"),
    path("contact/",views.contact,name="ContactUs"),
    path("signup/",views.handleSignup,name="handleSignup"),
    path("login/",views.handleLogin,name="handleLogin"),
    path("logout/",views.handleLogout,name="handleLogout"),
    url(r'^activate/(?P<activation_key>\w+)/$',views.activation_view,name='activation_view'),
]