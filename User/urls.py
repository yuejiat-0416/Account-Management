from django.urls import path
from .views import dashboard, CustomRegistrationView

urlpatterns = [
    path('', dashboard, name='homepage'),
    path('accounts/signup/', CustomRegistrationView.as_view(), name='custom_signup'),
]
