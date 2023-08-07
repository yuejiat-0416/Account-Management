from django.urls import path
from .views import dashboard, CustomRegistrationView

urlpatterns = [
    path('dashboard', dashboard, name='homepage'),
]
