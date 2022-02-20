from django.urls import path
from . import views
urlpatterns = [
    path('', views.index ),
    path('post/message', views.post_message),
    path('post/comment', views.post_comment),
    path('delete/message/<int:message_id>/<int:user_id>', views.delete_message),
    path('log_out', views.log_out),]