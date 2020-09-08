from django.urls import path

from booked.api.v1 import RoomAPI, BookedRoomAPI, OverviewAPI

urlpatterns = [
    path('room/<int:id>/', RoomAPI.as_view()),
    path('room/', RoomAPI.as_view()),
    path('room/overview/<int:id>/', OverviewAPI.as_view()),

    path('booked-room/<int:id>/', BookedRoomAPI.as_view()),
    path('booked-room/', BookedRoomAPI.as_view()),

]