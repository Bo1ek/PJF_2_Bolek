from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, CalendarEvent, Message2,Author

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(CalendarEvent)
admin.site.register(Message2)
admin.site.register(Author)
