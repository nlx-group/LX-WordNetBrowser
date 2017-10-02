from django.conf.urls import url
from .views import Renders, Initializer

urlpatterns = [
    url(r'^search/', Initializer.init),
    url(r'^references', Renders.references_render),
    url(r'^help', Renders.help_render),
    url(r'^', Renders.index),
]
