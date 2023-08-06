from django.urls import path
from .views import dashboard, JoinAccountView

urlpatterns = [
    path('', dashboard, name='homepage'),
    path('join_account', JoinAccountView.as_view(), name='join-account'),
]
