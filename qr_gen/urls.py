from django.urls import path

from .views import QrGenView

urlpatterns = [
    path("", QrGenView.as_view(), name="qr-gen"),
]
