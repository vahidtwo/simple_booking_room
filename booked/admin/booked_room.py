from core.admin import AbstractBaseAdmin


class BookedRoomAdmin(AbstractBaseAdmin):
    list_display = ('id', 'get_username', 'get_room_number', 'price', 'start_at', 'end_at', 'is_active')
    list_editable = ()
    search_fields = ('id', 'user__username', 'room__room_number')
    list_filter = ('room__room_number', 'user__username')
    list_select_related = ('room', 'user')

    def get_username(self, obj):
        return obj.user.username

    def get_room_number(self, obj):
        return obj.room.room_number

    get_username.short_description = 'username'
    get_room_number.short_description = 'room_number'


