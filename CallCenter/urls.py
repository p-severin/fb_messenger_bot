from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CallCenter.as_view())
]