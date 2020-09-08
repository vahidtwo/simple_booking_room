from booked.models import Room
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
