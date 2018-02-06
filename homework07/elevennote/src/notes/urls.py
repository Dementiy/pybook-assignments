from django.urls import path

from .views import (
    NoteList, NoteDetail, NoteCreate
)

app_name = 'notes'

urlpatterns = [
    path('', NoteList.as_view(), name='index'),
    path('<int:pk>/', NoteDetail.as_view(), name='detail'),
    path('new/', NoteCreate.as_view(), name='create'),
]
