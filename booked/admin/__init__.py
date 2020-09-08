from .booked_room import BookedRoomAdmin
from .room import RoomAdmin
from booked.models import Room, BookedRoom
from django.contrib import admin

admin.site.register(Room, RoomAdmin)
admin.site.register(BookedRoom, BookedRoomAdmin)