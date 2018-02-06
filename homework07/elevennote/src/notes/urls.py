from django.urls import path

from .views import NoteList, NoteDetail

app_name = 'notes'

urlpatterns = [
    path('', NoteList.as_view(), name='index'),
    path('<int:pk>/', NoteDetail.as_view(), name='detail'),
]
