from django.contrib import admin

from book.models import BookRoom, Room, BookedRoom, Listing
from core.admin import AbstractBaseAdmin


class RoomAdmin(AbstractBaseAdmin):
    list_display = ('id', 'room_number', 'has_good_view', 'is_vip', 'bed_count', 'size', "listing")
    list_editable = ('bed_count', 'size')
    search_fields = ('id', 'room_number')
    list_filter = ('is_vip', 'has_good_view', 'listing__name')


class BookRoomAdmin(AbstractBaseAdmin):
    list_display = ('id', 'get_username', 'get_room_number', 'price', 'start_at', 'end_at', 'is_active')
    list_editable = ()
    search_fields = ('id', 'room__listing__name', 'room__room_number')
    list_filter = ('room__room_number', 'room__listing__name')
    list_select_related = ('room__user',)

    def get_username(self, obj):
        return obj.room.user.username

    def get_room_number(self, obj):
        return obj.room.room_number

    get_username.short_description = 'username'
    get_room_number.short_description = 'room_number'


class ListingAdmin(AbstractBaseAdmin):
    list_display = ('user', 'name')
    list_filter = ('user',)



admin.site.register(Listing, ListingAdmin)
admin.site.register(BookRoom, BookRoomAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(BookedRoom)
