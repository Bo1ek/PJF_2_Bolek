from django.urls import path, include
from . import views
from .consumers import ChatConsumer

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/filter', views.CalendarView.as_view(), name='calendar_filter'),
    path('calendar_event/new/', views.calendar_event, name='calendar_event_new'),
    path('calendar_event/edit/(<str:event_id>)/', views.calendar_event, name='calendar_event_edit'),
    path('calendar_event/delete/(<str:event_id>)',views.calendar_event_delete, name='calendar_event_delete'),

    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),

    path('chat/', views.chat, name='chat'),
    path('create-message/', views.create_message, name='create-message'),
    path('stream-chat-messages/', views.stream_chat_messages, name='stream-chat-messages'),
]