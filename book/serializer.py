from accounts.serializer import UserSerializer
from book.models import BookRoom, BookedRoom
from book.models import Room
from core import serializers


class RoomSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.bed_count = validated_data.get('bed_count', instance.bed_count)
        instance.size = validated_data.get('size', instance.size)
        instance.is_vip = validated_data.get('is_vip', instance.is_vip)
        instance.has_good_view = validated_data.get('has_good_view', instance.has_good_view)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.room_number = validated_data.get('room_number', instance.room_number)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    class Meta:
        model = Room
        fields = '__all__'


class BookRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer(exclude=('priority', 'is_active', 'created_at', 'updated_at'), read_only=True)
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.room = validated_data.get('room', instance.room)
        instance.start_at = validated_data.get('start_at')
        instance.end_at = validated_data.get('end_at')
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    class Meta:
        model = BookRoom
        fields = '__all__'


class BookedRoomSerializer(serializers.ModelSerializer):
    book_room = BookRoomSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BookedRoom
        fields = "__all__"
