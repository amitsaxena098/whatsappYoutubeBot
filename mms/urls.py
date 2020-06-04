from django.urls import path

from .views import mms_reply

urlpatterns = [
    path('', mms_reply, name='mms_reply')
]
