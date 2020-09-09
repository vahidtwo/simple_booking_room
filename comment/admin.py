from django.contrib import admin

from comment.models import Comment
from core.admin import AbstractBaseAdmin


class CommentAdmin(AbstractBaseAdmin):
    list_display = ('id', 'get_listing', 'get_room', 'title')
    list_editable = ()
    search_fields = ('id', 'booked_room__book_room__room__listing__name', 'title')
    list_filter = ('rate', 'booked_room__book_room__room__room_number')
    list_select_related = ('booked_room__book_room__room',)

    def get_listing(self, obj):
        return obj.booked_room.book_room.room.listing.name

    def get_room(self, obj):
        return obj.booked_room.book_room.room.room_number

    get_room.short_description = 'room number'
    get_listing.short_description = 'listing'


admin.site.register(Comment, CommentAdmin)
