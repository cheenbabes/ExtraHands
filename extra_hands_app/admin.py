from django.contrib import admin
from extra_hands_app.models import Teacher, Client, Event, Available_Time, Email_List

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Available_Time)
admin.site.register(Email_List)