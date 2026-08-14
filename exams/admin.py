from django.contrib import admin

# Register your models here.
from .models import Exam,Notification


admin.site.register(Exam)
admin.site.register(Notification)