from django.contrib import admin

from comment.models import Comment
from core.admin import AbstractBaseAdmin


class CommentAdmin(AbstractBaseAdmin):
    list_display = ('id', 'get_user', 'get_room', 'title')
    list_editable = ()
    search_fields = ('id', 'user__username', 'title')
    list_filter = ('rate', 'booked_room__book_room__room__room_number')
    list_select_related = ('booked_room__book_room__room__room_number',)

    def get_user(self, obj):
        return obj.booked_room.user.username

    def get_room(self, obj):
        return obj.booked_room.book_room.room.room_number

    get_room.short_description = 'room number'
    get_user.short_description = 'user'


admin.site.register(Comment, CommentAdmin)
