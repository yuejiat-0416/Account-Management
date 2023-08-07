from django.urls import path
from .views import CreateAccountView, SendInviteView

urlpatterns = [
    path('create', CreateAccountView.as_view(), name='create'),
    path('invite', SendInviteView.as_view(), name='send-invite'),
    # path('create/useraccount', CreateUserAccountView.as_view(), name='create-user-account'),
]