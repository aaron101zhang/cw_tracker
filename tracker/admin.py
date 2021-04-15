from django.contrib import admin
from .models import AuthorizedUser, DailyData, Participant, PlayDate
# Register your models here.
admin.site.register(AuthorizedUser)
admin.site.register(DailyData)
admin.site.register(Participant)
admin.site.register(PlayDate)