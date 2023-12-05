from django.contrib import admin
from .models import studentHistory,GameHistory,GameLevel
# Register your models here.
admin.site.register(studentHistory)
admin.site.register(GameHistory)
admin.site.register(GameLevel)