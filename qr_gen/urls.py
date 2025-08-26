from django.urls import path

from .views import QrGenView, SaveQRCodeView

urlpatterns = [
    path("", QrGenView.as_view(), name="qr-gen"),
    path("save-qrcode/", SaveQRCodeView.as_view(), name="save-qrcode"),
]
