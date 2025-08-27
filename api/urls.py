from django.urls import path
from .views import QrGenAPIView, GetQrcodeAPIView, UserQrCodeAPIView

urlpatterns = [
    path("create-qrcode/", QrGenAPIView.as_view(), name="api-create-qrcode"),
    path(
        "get-qrcode/<int:qrcode_id>", GetQrcodeAPIView.as_view(), name="api-get-qrcode"
    ),
    path("user-qrcodes/", UserQrCodeAPIView.as_view(), name="api-user-qrcodes"),
]
