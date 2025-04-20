from django.contrib import admin
from .models import VotingStatus, AdminUser

admin.site.register(VotingStatus)
admin.site.register(AdminUser)