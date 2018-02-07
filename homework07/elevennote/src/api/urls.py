from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from .views import NoteViewSet

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register('notes', NoteViewSet)

urlpatterns = [
    path('jwt-auth/', obtain_jwt_token),
    path('', include(router.urls)),
]
