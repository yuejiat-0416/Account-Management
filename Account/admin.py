from django.contrib import admin
from .models import Account, UserAccount, TeamInvitation

admin.site.register(Account)
admin.site.register(UserAccount)
admin.site.register(TeamInvitation)
