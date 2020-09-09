from accounts.serializer import UserSerializer
from book.models import BookRoom, BookedRoom, Listing
from book.models import Room
from core import serializers


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()

    def update(self, instance, validated_data):
        instance.bed_count = validated_data.get('bed_count', instance.bed_count)
        instance.size = validated_data.get('size', instance.size)
        instance.is_vip = validated_data.get('is_vip', instance.is_vip)
        instance.has_good_view = validated_data.get('has_good_view', instance.has_good_view)
        instance.room_number = validated_data.get('room_number', instance.room_number)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    class Meta:
        model = Room
        fields = '__all__'


class BookRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer(exclude=('created_at', 'updated_at'), read_only=True)
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        instance.room = validated_data.get('room', instance.room)
        instance.price = validated_data.get('price', instance.price)
        instance.start_at = validated_data.get('start_at', instance.start_at)
        instance.end_at = validated_data.get('end_at', instance.end_at)
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
