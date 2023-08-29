from django.urls import path
from .views import CreateAccountView, SendInviteView, UpdateAccountInformationView

urlpatterns = [
    path('create', CreateAccountView.as_view(), name='create'),
    path('invite', SendInviteView.as_view(), name='send-invite'),
    path('information', UpdateAccountInformationView.as_view(), name='information'),
]