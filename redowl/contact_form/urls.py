from django.urls import path
from .views import tg_form

urlpatterns = [
    path("", tg_form, name="tg-forms"),
]
