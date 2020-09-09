from rest_framework import status
from rest_framework.views import APIView

from book.models import Room, Listing
from book.serializer import RoomSerializer
from core.http import JsonResponse


class RoomAPI(APIView):
    def get(self, request, id):
        try:
            return JsonResponse(data=RoomSerializer(Room.objects.get(pk=id)).data)
        except Room.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - room does not exists')

    def post(self, request):
        try:
            data = request.data
            room = Room()
            room.bed_count = data.get('bed_count')
            room.size = data.get('size')
            room.is_vip = data.get('is_vip')
            room.has_good_view = data.get('has_good_view')
            room.room_number = data.get('room_number')
            room.description = data.get('description')
            room.listing = Listing.objects.get(pk=data['listing_id'])
            room.save()
            return JsonResponse(status=status.HTTP_201_CREATED, message='create successful')
        except Listing.DoesNotExist:
            return JsonResponse(message='wrong id - listing not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse(message=str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            Room.objects.get(pk=id).delete()
            return JsonResponse(message='delete successful')
        except Room.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - room does not exists')
        except Exception as e:
            return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

    def put(self, request, id):
        try:
            data = dict(request.data)
            room = Room.objects.get(pk=id)
            try:
                listing = Listing.objects.get(pk=data['listing_id'])
            except Listing.DoesNotExist:
                listing = None
            ser = RoomSerializer(room, data)
            if ser.is_valid():
                if listing:
                    ser.save(listing=listing)
                else:
                    ser.save()
                return JsonResponse(message='update successful')
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, message=ser.errors)
        except Room.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, message='wrong id - room does not exists')
        except Exception as e:
            return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
