from django.contrib import admin
from .models import Account, UserAccount, TeamInvitation, UserRole, Role

admin.site.register(Account)
admin.site.register(UserAccount)
admin.site.register(TeamInvitation)
admin.site.register(UserRole)
admin.site.register(Role)
