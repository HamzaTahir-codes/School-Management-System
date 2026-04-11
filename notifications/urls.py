from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='index'),
    path('inbox/', views.NotificationListView.as_view(), name='inbox'),
    path('broadcast/add/', views.BroadcastCreateView.as_view(), name='broadcast_add'),
    path('unread-count/', views.UnreadCountView.as_view(), name='unread_count'),
    
    # Interactive Endpoints
    path('mark-read/', views.MarkReadView.as_view(), name='mark_read'),
    path('delete/', views.DeleteMessageView.as_view(), name='delete_message'),
    path('reply/', views.ReplyCreateView.as_view(), name='reply_create'),
]