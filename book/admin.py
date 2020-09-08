from django.contrib import admin

from book.models import BookRoom, Room, BookedRoom
from core.admin import AbstractBaseAdmin


class RoomAdmin(AbstractBaseAdmin):
    list_display = ('id', 'room_number', 'has_good_view', 'is_vip', 'bed_count', 'size', "user")
    list_editable = ('bed_count', 'size')
    search_fields = ('id', 'room_number', 'user__username')
    list_filter = ('is_vip', 'has_good_view', 'user__username')


class BookRoomAdmin(AbstractBaseAdmin):
    list_display = ('id', 'get_username', 'get_room_number', 'price', 'start_at', 'end_at', 'is_active')
    list_editable = ()
    search_fields = ('id', 'room__user__username', 'room__room_number')
    list_filter = ('room__room_number', 'room__user__username')
    list_select_related = ('room__user',)

    def get_username(self, obj):
        return obj.room.user.username

    def get_room_number(self, obj):
        return obj.room.room_number

    get_username.short_description = 'username'
    get_room_number.short_description = 'room_number'


admin.site.register(BookRoom, BookRoomAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(BookedRoom)
