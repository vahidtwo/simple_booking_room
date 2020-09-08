from django.urls import path

from book.api.v1 import RoomAPI, BookRoomAPI, OverviewAPI, BookedRoomAPI

urlpatterns = [
    path('room/<int:id>/', RoomAPI.as_view()),
    path('room/', RoomAPI.as_view()),
    path('room/overview/<int:id>/', OverviewAPI.as_view()),

    path('book-room/<int:id>/', BookRoomAPI.as_view()),
    path('book-room/', BookRoomAPI.as_view()),
    path('book-room/booking/', BookedRoomAPI.as_view()),
    path('book-room/booking/<int:id>/', BookedRoomAPI.as_view())


]