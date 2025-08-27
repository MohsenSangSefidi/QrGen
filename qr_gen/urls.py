from django.urls import path

from .views import QrGenView, SaveQRCodeView, ApiDocumentionView

urlpatterns = [
    path("", QrGenView.as_view(), name="qr-gen"),
    path("save-qrcode/", SaveQRCodeView.as_view(), name="save-qrcode"),
    path("api-doc/", ApiDocumentionView.as_view(), name="api-doc"),
]
