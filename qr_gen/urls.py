from django.urls import path

from .views import QrGenView, Footer, Header

urlpatterns = [
    path('', QrGenView.as_view(), name='qr-gen'),

    path('header/', Header.as_view(), name='header'),
    path('footer/', Footer.as_view(), name='footer'),
]
