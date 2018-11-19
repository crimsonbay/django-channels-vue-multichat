from django.conf.urls import url
from rest_framework import routers
from .views import UserViewSet, MessageViewSet, index, room
router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('new_message', MessageViewSet)
urlpatterns = router.urls
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]
